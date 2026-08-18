from odoo.http import request

def valid_response(data , message="Done" , status = 200 , pagination_info = ""):
    body = {
        'data':data,
        'message':message
        }

    
    if pagination_info:
        body['pagination_info'] = pagination_info

    return request.make_json_response(body , status= status)

def invalid_response(error , status=400):
    body = {
        'error':error,
    }


    return request.make_json_response(body , status=status)