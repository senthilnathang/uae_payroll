odoo.define('hr_payroll_uae.payroll', function (require) {
"use strict";

require('web.dom_ready');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
var Widget = require('web.Widget');


var Payroll = Widget.extend({
    events: {
        'click #btn_drafted_payslips': 'testing_function',
    },
    init: function(){
        var self = this;
    },
    testing_function: function() {
        event.preventDefault();
        alert('here');
    }
});

new Payroll();
});
