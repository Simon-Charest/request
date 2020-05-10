#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright 2019, SLCIT inc.'
__credits__ = []
__email__ = 'simoncharest@gmail.com'
__license__ = 'GPL'
__maintainer__ = 'Simon Charest'
__project__ = 'Request'
__status__ = 'Developement'
__version__ = '1.0.0'

import asyncio
import aiohttp
import json
import requests


def main():
    loop = asyncio.get_event_loop()

    try:
        task = loop.create_task(initialize_requests())
        loop.run_until_complete(task)

    finally:
        loop.close()


async def initialize_requests():
    # Hyundai Elantra 2016
    blax_url = 'http://vxp.uat.blax.host/orbit/products/19/1449/32011'

    url = 'http://es.belroncanada.dev'
    data = {}
    headers = {'Content-Type': 'application/json', 'ActionId': 'null'}
    phone_number_url = '/PhoneNumber/PhoneNumberService.svc/json/GetOlbPhoneNumber'
    phone_number_data = {'olbEntry': '0'}
    location_url = '/Location/LocationService.svc/json/GetLocationByCode'
    location_data = data
    vehicle_url = '/Vehicle/VehicleService.svc/json/GetVehicleFromVin'
    vehicle_data = data
    part_funneling_url = '/PartFunneling/PartFunnelingService.svc/external/json/GetPartsForReplacementExternal'
    part_funneling_data = {'partRequest': {'RequestId': '0000-0000', 'CarId': 'CR00000001', 'GlassType': 'WS',
                                           'LocationCode': '6101'}}
    price_packaging_url = '/PricePackaging/PricePackagingService.svc/json/GetOffersExternal'
    price_packaging_data = {'priceRequest': {'PartNumber':
                                             'DABBA52827200CEC2EFEFDA39A44CBBBD138F14838271FD78F2FAD8AF069B403',
                                             'CarId': 'CR00000001', 'LocationCode': '6101', 'TransactionId':
                                             '00000000-0000-0000-0000-000000000000'}}
    mailing_list_url = '/MailingList/MailingListService.svc/json/SendMail'
    mailing_list_data = data
    tax_url = '/Tax/TaxService.svc/external/json/GetTaxDetailsExternal'

    # TODO: Fix this date
    tax_data = {'parts': [{'Quantity': 0, 'Amount': 0.00, 'Code':
                'DABBA52827200CEC2EFEFDA39A44CBBBD138F14838271FD78F2FAD8AF069B403'}], 'provinceCode': 'QC', 'date':
                '\\/Date(0000000000000+0000)\\/'}
    booking_url = '/Booking/BookingService.svc/external/json/GetAvailableSchedulesByShopExternal'
    booking_data = {'locationCode': '6101', 'workType': 'installation', 'workPlaceType': 'InShop'}
    work_order_url = '/WorkOrder/WorkOrderService.svc/json/CreateWrkOLBExternal'

    # TODO: Fix this date
    work_order_data = {'workorder': {'AppointmentStart': '\\/Date(0000000000000+0000)\\/', 'WorkType': 'Installation',
                                     'LocationCode': '6101', 'ServiceType': 'InShop', 'GlassType': 'NonGlass',
                                     'context': 'OLB'}}
    requests_ = []

    async with aiohttp.ClientSession() as session:
        requests_.append(get_request_async(session, blax_url))
        # requests_.append(post_request_async(session, url + phone_number_url, phone_number_data, headers))
        # requests_.append(post_request_async(session, url + location_url, location_data, headers))
        # requests_.append(post_request_async(session, url + vehicle_url, vehicle_data, headers))

        # Execute them all at once
        await asyncio.gather(*requests_)


async def get_request_async(session, url):
    async with session.get(url) as response:
        data = await response.text()
        print(data)
        dump('response.json', data)


async def post_request_async(session, url, data, headers):
    async with session.post(url, data=data, headers=headers) as response:
        data = await response.text()
        print(data)


def get_request(url):
    return requests.get(url).json()


def post_request(url, data, headers):
    return requests.post(url, data=json.dumps(data), headers=headers)


def dump(file_path, data):
    json.dump(data, open(file_path, 'w'))


def read(file_path):
    return json.load(open(file_path))


def print_values(values, key):
    for value in values:
        print(values[value][key])


main()
