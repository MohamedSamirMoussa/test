import json
import math
from odoo import http
from odoo.http import request
from urllib.parse import parse_qs
from .handling_response import valid_response , invalid_response


class PropertyApi(http.Controller):
    # Create Property API
    @http.route("/v1/property" , methods=["POST"] , type="http" , csrf=False , auth="none")
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            values = json.loads(args)
            env = request.env(user=1)
            res = env['property'].sudo().create(values)
            
            if res:
                return valid_response({
                "id":res.id,
                "name":res.name,
                "active":res.active,
                "message": f"Property {res.name} Created Successfully",
            } , status=201)
        except Exception as error:
            return invalid_response(
                            {
                                "Error": error
                            },
                            status=400
                        )

    #Get All Properties and filtered with state
    @http.route("/v1/property" , methods=["GET"] , type="http" , auth="none" , csrf=False)
    def get_all_properties(self):
        query = parse_qs(request.httprequest.query_string.decode('utf-8'))
        query_domain = []
        page = offset = None
        limit = 5

        if query:
            if query.get('limit'):
                limit = int(query.get('limit')[0])
            if query.get('page'):
                page = int(query.get('page')[0])

        if page:
            offset = (page * limit) - limit

        if query.get('state'):
            query_domain += [('state' , '=' , query.get('state')[0])]

        count = request.env['property'].sudo().search_count(query_domain)
        property_ids = request.env['property'].sudo().search(query_domain, offset=offset,limit=limit )
        if not property_ids.exists():
                    return invalid_response({
                        "message":"No Property Found",
                    }, status=404)
        return valid_response({
            "pagination_info": {
                        'page' : page if page else 1,
                        'pages': math.ceil(count / limit) if limit else 1,
                        'count': count,
                        'limit': limit,                    },
            "properties" : [
                {
                    "id":property.id,
                    "name":property.name,
                    "state":property.state,
                    "active":property.active
                }
                for property in property_ids
            ]
        })

    # Get one property with id 
    @http.route("/v1/property/<int:property_id>" , methods=["GET"] , type="http" , csrf=False , auth="none")
    def get_property(self , property_id):
        res = request.env['property'].sudo().browse(property_id)
        if not res.exists():
            return invalid_response({
                "message":"Property Not Found",
            }, status=404)

        return valid_response({
            "id":res.id, 
            "name":res.name, 
            "active":res.active,
        })

    # Update one property with id
    @http.route("/v1/property/<int:property_id>" , methods=["PUT"] , auth="none" , type="http" , csrf=False)
    def update_property(self , property_id):
        try:
            property_id = request.env["property"].sudo().search([
                        ("id", "=" , property_id)
                    ])
            args = request.httprequest.data.decode()
            values = json.loads(args)
            property_id.write(values)
            return valid_response(
                {
                "Message":f"Property {property_id} updated successfully"
                },
                status=202
                )
        except Exception as error:
            return invalid_response(
                {
                    "Error": error
                },
                status=400
            )


    # Delete One Property with id
    @http.route("/v1/property/<int:property_id>" , methods=["DELETE"] , auth="none" , type="http" , csrf=False)
    def delete_property(self , property_id):
        try:
            property_id = request.env['property'].sudo().search([
                            ('id' , '=' , property_id)
                            ])
            if not property_id:
                return invalid_response({
                                "Message" : "Property not found"
                            } , status=404)
            property_id.unlink()
            return valid_response(
                {
                "Message":"Property Deleted Successfully"
                },
                status=200)
        except Exception as error:
            return invalid_response(
                            {
                                "Error": error
                            },
                            status=400
                        )