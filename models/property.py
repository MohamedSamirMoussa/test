from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import requests

class Property(models.Model):
    _name = 'property'
    _description = 'Real Estate Properties'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # tne name and desc of the property
    name = fields.Char(required=True, default="New")
    description = fields.Text(tracking=1)
    ref = fields.Char(default="new", readonly=True, copy=False)
    # specs of prop
    post_code = fields.Char(required=True)
    date_availability = fields.Date(required=True,  tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float(digits=(0, 2))
    selling_price = fields.Float(digits=(0, 2))
    bedrooms = fields.Integer(required=True, default=1)
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=0)
    garage_area = fields.Integer()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')
    # owner model
    owner_id = fields.Many2one('owner')
    owner_name = fields.Char(
        related='owner_id.owner_name',
        readonly=False
    )
    owner_phone = fields.Char(related='owner_id.owner_phone')
    owner_address = fields.Char(related='owner_id.owner_address')
    active = fields.Boolean(default=True)
    # Room model
    room_ids = fields.One2many('room', 'property_id')
    total_area = fields.Float(compute='_compute_total_area', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default="draft")

    _sql_constraints = [(
        'unique_name',
        'unique("name")',
        'This name already exist'
    )]
    # Validation With Decorators

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for rec in self:
            if rec.bedrooms < 1:
                raise ValidationError("Bedrooms must be at least 1")

    @api.constrains('selling_price', 'expected_price', 'facades', 'garden_area', 'garage_area')
    def _check_negative_values(self):
        for rec in self:
            fields_to_check = {
                "Selling Price": rec.selling_price,
                "Expected Price": rec.expected_price,
                "Facades": rec.facades,
                "Garden Area": rec.garden_area,
                "Garage Area": rec.garage_area,
            }

        for field_name, value in fields_to_check.items():
            if value < 0:
                raise ValidationError(
                    f"{field_name} cannot be negative."
                )
                
    @api.onchange('bedrooms')
    def _onchange_bedrooms(self):
        if self.bedrooms > 5:
            self.garden = True
            self.garden_area = 20
        
    def open_change_state(self):
        self.ensure_one()
        
        if self.state != "closed":
            raise UserError("Change State is available only when the property is Closed.")
        
        action = self.env["ir.actions.actions"]._for_xml_id("app_one.change_state_wizard_action")   
        action["context"] = {
            'default_property_id': self.id 
        }
        return action
        
    @api.depends(
        "room_ids.area",
        "garden",
        "garden_area",
        "garage",
        "garage_area",
    )
    def _compute_total_area(self):
        for rec in self:
            total = sum(rec.room_ids.mapped('area'))
            if rec.garden:
                total += rec.garden_area
            if rec.garage:
                total += rec.garage_area
            rec.total_area = total

    def unlink(self):
        for rec in self:
            if rec.state == 'sold':
                raise ValidationError(
                    "Sold Property can't be deleted."
                )
        return super().unlink()
    def create_history_rec(self, old_state, new_state, reason=""):
            for rec in self:
                rec.env['property.history'].create({
                    'user_id': self.env.uid,
                    'property_id': rec.id,
                    'old_state': old_state,
                    'new_state': new_state,
                    'reason': reason or "",
    })     
               
    def change_state_action(self, state):
        changes = {
            'draft': ['pending', 'closed'],
            'pending': ['draft', 'sold', 'closed'],
            'sold': ['closed'],
            'closed': []
        }
        
        for rec in self:
            if state not in changes[rec.state]:
                raise UserError(f'You cannot change form {rec.state} to {state}')
            rec.create_history_rec(rec.state, state)
            rec.write({
                "state": state
            })
            
    
    def action_draft(self):
        self.change_state_action('draft')
    
    def action_pending(self):
        self.change_state_action('pending')
    
    def action_sold(self):
        self.change_state_action('sold')
    
    def action_closed(self):
        self.change_state_action('closed')
    
    def _check_selling_price(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True
        
    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        for rec in res:
            if rec.ref == 'new':
                rec.ref = self.env['ir.sequence'].next_by_code('property_seq')

        return res
    
    def property_xlsx_report(self):
        
        
        return {
            'type': 'ir.actions.act_url',
             'url': f'/property/excel/report/{self.env.context.get("active_ids")}',
             'target': 'new'
        }