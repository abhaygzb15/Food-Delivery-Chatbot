import re
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()
inprogress_orders = {}


@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary info from the payload
    # based on the structure of the WebHookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    # these are the intents which u have to made in the dialogflow console.
    intent_handler_dict = {
        "order.add - context: ongoing-order": add_to_order,
        "order.remove - context: ongoing-order": remove_from_order,
        "order.complete - context: ongoing-order": complete_order,
        "track.order - context: ongoing-tracking": track_order,
        "new.order": new_order  # Handle new order intent
    }

    if intent in intent_handler_dict:
        return intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={
            "fulfillmentText": "Sorry, I didn't understand that. Can you please repeat?"
        })


def new_order(parameters: dict, session_id: str):
    # Clear any existing order for the session
    if session_id in inprogress_orders:
        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": "Ok, starting a new order. You can say things like 'I want two pizzas and one mango lassi'. "
                           "Make sure to specify a quantity for every food item! Also, we have only the following items on our menu: "
                           "Pav Bhaji, Chole Bhature, Pizza, Mango Lassi, Masala Dosa, Biryani, Vada Pav, Rava Dosa, and Samosa."
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "Sorry! I'm having trouble finding your order. Can you place the order again?"
        })

    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]
    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    fulfillment_text = ""
    if len(removed_items) > 0:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order! "

    if len(no_such_items) > 0:
        fulfillment_text += f"Your current order does not have {', '.join(no_such_items)}. "

    if len(current_order) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify the food item and quantity?"
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having trouble finding your order. Can you place the order again?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. Please place a new order again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order. Here is your order id #{order_id}. Your order total is {order_total} which you can pay on delivery."

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")
    return next_order_id


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with the order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

