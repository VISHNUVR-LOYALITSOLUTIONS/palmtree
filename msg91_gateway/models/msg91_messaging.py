# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from urllib3.exceptions import HTTPError

import logging
_logger = logging.getLogger(__name__)

# from urllib2 import Request, urlopen
# from urllib import urlencode
import json
import base64
from .msg91 import MSG91Client


def send_sms_using_msg91(body_sms, mob_no, from_mob=None, sms_gateway=None):
    '''
    This function is designed for sending sms using clicksend SMS API.

    :param body_sms: body of sms contains text
    :param mob_no: Here mob_no must be string having one or more number seprated by (,)
    :param from_mob: sender mobile number or id used in Clicksend API
    :param sms_gateway: sms.mail.server config object for Clicksend Credentials
    :return: response dictionary if sms successfully sent else empty dictionary
    '''
    if not sms_gateway or not body_sms or not mob_no:
        return {}
    if sms_gateway.gateway == "msg91":
        msg91_api_key = sms_gateway.msg91_api_key
        try:
            if msg91_api_key:
                client = MSG91Client(api_key=msg91_api_key)
                msg_list = []
                for mobi_no in mob_no.split(','):
                    return MSG91Client.send_sms(
                        client, message=body_sms, mobile=str(
                            mobi_no))
        except HTTPError as e:
            _logger.info(
                "---------------MSG91 HTTPError While Sending SMS ----%r---------", e)
            return {}
        except Exception as e:
            _logger.info(
                "---------------MSG91 Exception While Sending SMS -----%r---------", e)
            return {}
    return {}


class SmsSms(models.Model):
    """SMS sending using MSG91 SMS Gateway."""

    _inherit = "sms.sms"
    # _name = "sms.smsmail"
    _description = "MSG91 SMS"

    def send_sms_via_gateway(self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(SmsSms, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'msg91':
                msg91_api_key = gateway_id.msg91_api_key
                for element in mob_no:
                    for mobi_no in element.split(','):
                        response = send_sms_using_msg91(
                            body_sms, element, from_mob=from_mob, sms_gateway=gateway_id)
                        sms_report_obj = self.env["sms.report"].create(
                            {'to': mobi_no, 'msg': body_sms, 'sms_sms_id': self.id, "auto_delete": self.auto_delete,
                             'sms_gateway_config_id': gateway_id.id})
                        if response.get("type") == "success":
                            if response.get("message"):

                                sms_report_obj.write(
                                    {'state': 'sent', 'msg91_api_key': msg91_api_key, 'msg91_message_id': response.get("message")})
                        elif response.get("type") == "error":
                            sms_report_obj.write({'state': 'error'})
                        else:
                            sms_report_obj.write({'state': 'new'})
                    else:
                        self.write({'state': 'error'})
                else:
                    self.write({'state': 'sent'})
            else:
                gateway_id = super(SmsSms, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        else:
            _logger.info(
                "----------------------------- SMS Gateway not found -------------------------")
        return gateway_id


class SmsReport(models.Model):
    """SMS report."""

    _inherit = "sms.report"

    msg91_message_id = fields.Char("MSG91 SMS ID")
    msg91_api_key = fields.Char("MSG91 API Key")

    def send_sms_via_gateway(self, body_sms, mob_no, from_mob=None, sms_gateway=None):
        self.ensure_one()
        gateway_id = sms_gateway if sms_gateway else super(SmsReport, self).send_sms_via_gateway(
            body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        if gateway_id:
            if gateway_id.gateway == 'msg91':
                msg91_api_key = gateway_id.msg91_api_key
                for element in mob_no:
                    count = 1
                    for mobi_no in element.split(','):
                        if count == 1:
                            self.to = mobi_no
                            rec = self
                        else:
                            rec = self.create(
                                {'to': mobi_no,
                                 'msg': body_sms,
                                 "auto_delete": self.auto_delete,
                                 'sms_gateway_config_id': gateway_id.id})
                        response = send_sms_using_msg91(
                            body_sms, mobi_no, from_mob=from_mob, sms_gateway=gateway_id)
                        if response.get("type") == "success":
                            if response.get("message"):
                                sms_report_obj = self.env["sms.report"].create(
                                    {'to': mobi_no, 'msg': body_sms, 'sms_sms_id': self.id, "auto_delete": self.auto_delete, 'sms_gateway_config_id': gateway_id.id})
                                sms_report_obj.write(
                                    {'state': 'sent', 'msg91_api_key': msg91_api_key, 'msg91_message_id': response.get("message")})
                        elif response.get("type") == "error":
                            sms_report_obj.write({'state': 'undelivered'})
                        count += 1
            else:
                gateway_id = super(SmsReport, self).send_sms_via_gateway(
                    body_sms, mob_no, from_mob=from_mob, sms_gateway=sms_gateway)
        return gateway_id
