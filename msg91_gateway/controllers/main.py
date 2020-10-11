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

import logging
from odoo.http import request
from odoo import http, SUPERUSER_ID
from odoo.exceptions import Warning
import requests
import urllib
import json
import base64
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)
import ast


class MSG91Notify(http.Controller):
    @http.route(['/msg91/notification'], type='http', auth='public', website=True, csrf=False)
    def msg91_notification(self, **post):
        """ msg91 notification controller"""
        # post = [
        #     {
        #         "requestId": "59e61886c01f466d0e8b4583",
        #         "userId": "38229",
        #         "report": [
        #             {
        #                 "desc": "Delivered",
        #                 "status": "1",
        #                 "number": "+919555065708",
        #                 "date": "2015-06-10 17:09:32.0"
        #             },
        #             {
        #                 "desc": "REJECTED",
        #                 "status": "16",
        #                 "number": "91XXXXXXXXXX",
        #                 "date": "2015-06-10 17:09:32.0"
        #             }
        #         ],
        #         "senderId": "tester"
        #     },
        #     {
        #         "requestId": "59f730a2c8f9091e6c8b4575",
        #         "userId": "38229",
        #         "report": [
        #             {
        #                 "desc": "Delivered",
        #                 "status": "1",
        #                 "number": "+919555065708",
        #                 "date": "2015-06-10 17:09:32.0"
        #             },
        #             {
        #                 "desc": "REJECTED",
        #                 "status": "16",
        #                 "number": "91XXXXXXXXXX",
        #                 "date": "2015-06-10 17:09:32.0"
        #             }
        #         ],
        #         "senderId": "tester"
        #     }
        # ]
        _logger.info(
            "WEBKUL DEBUG FOR MSG91: SUMMARY(POST DATA)%r", post)
        all_sms_report = request.env["sms.report"].sudo().search(
            [('state', 'in', ('sent', 'new'))])
        for sms in all_sms_report:
            if sms.msg91_message_id and sms.msg91_api_key:
                sms_sms_obj = sms.sms_sms_id
                sms.status_hit_count += 1
                content = eval(post.get('data'))
                for data in content:
                    if data.get('requestId') == sms.msg91_message_id:
                        for report in data.get('report'):
                            number = str(sms.to).split(
                                '+')[1] if str(sms.to).startswith('+') else str(sms.to)
                            if str(report.get('number')) == number:
                                if report.get('status') == '16':
                                    sms.state = "new"
                                if report.get('status') == '1':
                                    if sms.auto_delete:
                                        sms.sudo().unlink()
                                        request._cr.commit()
                                        if sms_sms_obj.auto_delete and not sms_sms_obj.sms_report_ids:
                                            sms_sms_obj.sudo().unlink()
                                            request._cr.commit()
                                        break
                                    else:
                                        sms.state = "delivered"
                                        request._cr.commit()
                                if report.get('status') == '2':
                                    sms.state = "undelivered"
                                    request._cr.commit()
        return {}
