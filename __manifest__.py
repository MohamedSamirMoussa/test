{
    'name': 'App One',
    'author': 'Mohamed Samir Moussa',
    'category': 'Real Estate',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale_management',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/sale_order.xml',
        'views/property_history.xml',
        'reports/property_report.xml',
        'wizard/change_state_view_wizard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/property.css',
            'app_one/static/src/components/listView/listView.xml',
            'app_one/static/src/components/listView/listView.js',
            'app_one/static/src/components/listView/listView.css',
            'app_one/static/src/components/formView/formView.xml',
            'app_one/static/src/components/formView/formView.js',
            'app_one/static/src/components/formView/formView.css',
            ],
    },
    'images': [
        'static/description/icon.png'
    ],
    'application': True,
    'installable': True,
}