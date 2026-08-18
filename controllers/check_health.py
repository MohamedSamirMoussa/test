from odoo import http


class CheckHealth(http.Controller):

    @http.route(
        "/api/check-health",
        methods=["GET"],
        type="http",
        auth="none",
        csrf=False
    )
    def check_health(self):
        return http.Response(
            '{"status": 200, "message": "Server Running"}',
            content_type="application/json",
            status=200
        )