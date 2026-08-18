/* @odoo-module */

import { Component, useState, onWillUnmount, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormView } from "../formView/formView"

class ListView extends Component {
    static template = "app_one.ListView";
    static components = {
        FormView
    }
    setup() {
        this.state = useState({
            records: []
        });
        this.orm = useService("orm");
        this.notification = useService("notification");

        onWillStart(async () => {
            await this.loadRecords();
        });

        this.updateRecords = setInterval(() => this.loadRecords(), 3000);

        onWillUnmount(() => clearInterval(this.updateRecords));
    }

    loadRecords = async () => {
        const result = await this.orm.searchRead("property", [], []);
        console.log(result);
        this.state.records = result;
    }


    deleteRecord = async (id) => {
        await this.orm.unlink("property", [id])

        this.notification.add("Property Deleted", { type: "warning" })

    }

    toggleViewForm() {
        this.state.showPropertyForm = !this.state.showPropertyForm
    }
}

registry.category("actions").add("app_one.action_list_view", ListView);