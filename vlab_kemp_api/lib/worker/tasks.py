# -*- coding: UTF-8 -*-
"""
Entry point logic for available backend worker tasks
"""
from celery import Celery
from vlab_api_common import get_task_logger

from vlab_kemp_api.lib import const
from vlab_kemp_api.lib.worker import vmware

app = Celery('kemp', backend='rpc://', broker=const.VLAB_MESSAGE_BROKER)


@app.task(name='kemp.show', bind=True)
def show(self, username, txn_id):
    """Obtain basic information about Kemp

    :Returns: Dictionary

    :param username: The name of the user who wants info about their default gateway
    :type username: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_KEMP_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        info = vmware.show_kemp(username)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    else:
        logger.info('Task complete')
        resp['content'] = info
    return resp


@app.task(name='kemp.create', bind=True)
def create(self, username, machine_name, image, network, txn_id):
    """Deploy a new instance of Kemp

    :Returns: Dictionary

    :param username: The name of the user who wants to create a new Kemp
    :type username: String

    :param machine_name: The name of the new instance of Kemp
    :type machine_name: String

    :param image: The image/version of Kemp to create
    :type image: String

    :param network: The name of the network to connect the new Kemp instance up to
    :type network: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_KEMP_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        resp['content'] = vmware.create_kemp(username, machine_name, image, network, logger)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    logger.info('Task complete')
    return resp


@app.task(name='kemp.delete', bind=True)
def delete(self, username, machine_name, txn_id):
    """Destroy an instance of Kemp

    :Returns: Dictionary

    :param username: The name of the user who wants to delete an instance of Kemp
    :type username: String

    :param machine_name: The name of the instance of Kemp
    :type machine_name: String

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_KEMP_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    try:
        vmware.delete_kemp(username, machine_name, logger)
    except ValueError as doh:
        logger.error('Task failed: {}'.format(doh))
        resp['error'] = '{}'.format(doh)
    else:
        logger.info('Task complete')
    return resp


@app.task(name='kemp.image', bind=True)
def image(self, txn_id):
    """Obtain a list of available images/versions of Kemp that can be created

    :Returns: Dictionary

    :param txn_id: A unique string supplied by the client to track the call through logs
    :type txn_id: String
    """
    logger = get_task_logger(txn_id=txn_id, task_id=self.request.id, loglevel=const.VLAB_KEMP_LOG_LEVEL.upper())
    resp = {'content' : {}, 'error': None, 'params': {}}
    logger.info('Task starting')
    resp['content'] = {'image': vmware.list_images()}
    logger.info('Task complete')
    return resp
