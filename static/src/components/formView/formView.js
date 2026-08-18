/* @odoo-module */


import { Component, useState, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FormView extends Component {

    static template = "app_one.FormView"

    setup() {
        this.state = useState({
            name: '',
            post_code: 0,
            date_availability: '',
            state: '',
            selling_price: 0,
            garden: false,
            garage: false,
            garden_orientation: ''
        })

        this.orm = useService("orm")
        this.notification = useService("notification")
    }

    async createRecord() {
        await this.orm.create("property", [{
            name: this.state.name,
            post_code: this.state.post_code,
            date_availability: this.state.date_availability,
            state: this.state.state,
            selling_price: this.state.selling_price,
            garden: this.state.garden,
            garage: this.state.garage,
            garden_orientation: this.state.garden_orientation,
        }])

        this.notification.add("Property Created ✔", { type: "success" })
    }

    close() {
        this.name = '';
        this.post_code = 0;
        this.date_availability = '';
        this.state = '';
        this.selling_price = 0;
        this.garden = false;
        this.garage = false;
        this.garden_orientation = '';
        this.props.onClose();
    }
}
