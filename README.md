# App One — Odoo Real Estate Module

An Odoo 18 learning module for property management. It covers core ORM models, computed fields, constraints, state history, security groups, reports, wizards, REST-style controllers, translations, and custom OWL view components.

## Features

- Property, owner, room, client, and history models
- Computed property totals and areas
- Validation and SQL constraints
- Draft, pending, sold, and closed property states
- Automatic state-change history
- Sale order integration
- Role-based security and access controls
- Property PDF report
- XLSX property export wizard
- JSON API controllers and health check
- Arabic translation resources
- Custom OWL list and form view components
- Custom backend styling

## Tech Stack

- Odoo 18 Community Edition
- Python 3.11
- PostgreSQL
- XML and QWeb
- OWL JavaScript components
- XLSX reporting

## Main Models

| Model | Purpose |
| --- | --- |
| property | Core property record and workflow |
| owner | Property owners |
| room | Rooms linked to properties |
| property.history | State-change audit trail |
| client | Client data |
| sale.order | Extended Odoo sales orders |
| change.state | State-change wizard |

## Installation

The manifest refers to module assets through the app_one namespace, so place the code in a directory named app_one inside your custom add-ons directory:

~~~bash
git clone https://github.com/MohamedSamirMoussa/test.git app_one
~~~

Add the parent folder to addons_path, update the app list, and install App One.

~~~bash
python odoo-bin -c odoo.conf -d YOUR_DATABASE -u app_one
~~~

## Dependencies

- base
- sale_management
- mail

## Development Note

The repository currently contains generated Python cache files and a Windows installer under i18n. These artifacts are not required by the module and should be removed from version control in a future cleanup commit.

## License

LGPL-3, as declared in the Odoo manifest.

## Author

[Mohamed Samir Moussa](https://github.com/MohamedSamirMoussa)
