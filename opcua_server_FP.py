import logging
import asyncio
import sys
import psutil
import random
import time
from asyncua import Server, ua
from asyncua.common.methods import uamethod

sys.path.insert(0, "..")

# Configure logger
logging.basicConfig(
    format=f'%(asctime)s %(levelname)-8s: %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
_logger = logging.getLogger('asyncua')

async def main():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/opcua_server/')
    server.set_server_name("Kaixo MUndua OPCUA")

    # setup our own namespace
    uri = 'http://examples.mondragon.edu/opcua'
    idx = await server.register_namespace(uri)
    print(idx)
    
    @uamethod
    async def air_conditioner_1ToON(parent):
        await air_conditioner_1_state.write_value("on")
        return 'air_conditioner_1 switched to ON'
    @uamethod
    async def air_conditioner_1ToOFF(parent):
        await air_conditioner_1_state.write_value("off")
        return 'air_conditioner_1 switched to OFF'
    @uamethod
    async def air_conditioner_2ToON(parent):
        await air_conditioner_2_state.write_value('on')
        return 'air_conditioner_2 switched to ON'
    @uamethod
    async def air_conditioner_2ToOFF(parent):
        await air_conditioner_2_state.write_value('off')
        return 'air_conditioner_2 switched to OFF'
    @uamethod
    async def air_conditioner_3ToON(parent):
        await air_conditioner_3_state.write_value('on')
        return 'air_conditioner_3 switched to ON'
    @uamethod
    async def air_conditioner_3ToOFF(parent):
        await air_conditioner_3_state.write_value('off')
        return 'air_conditioner_3 switched to OFF'
    
    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects
    # Create object
    air_conditioner_1 = await objects.add_object(
        ua.NodeId('air_conditioner_1', idx),
        'air conditioner 1'
    )
    air_conditioner_2 = await objects.add_object(
        ua.NodeId('air_conditioner_2', idx),
        'air conditioner 2'
    )
    air_conditioner_3 = await objects.add_object(
    ua.NodeId('air_conditioner_3', idx),
    'air conditioner 3'
    )

    air_conditioner_2_state = await air_conditioner_2.add_variable(
        ua.NodeId('air_conditioner_2/state', idx),
        'state3',
        'off'
    )
    air_conditioner_3_state = await air_conditioner_3.add_variable(
        ua.NodeId('air_conditioner_3/state', idx),
        'state2',
        'off'
    )

    air_conditioner_1_state = await air_conditioner_1.add_variable(
        ua.NodeId('air_conditioner_1/State', idx),
        'state1',
        'off'
    )

    # Add methods
    await air_conditioner_1.add_method(
        ua.NodeId('air_conditioner_1/switch_on', idx),
        'switch_on',
        air_conditioner_1ToON,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    await air_conditioner_1.add_method(
        ua.NodeId('air_conditioner_1/switch_off', idx),
        'switch_off',
        air_conditioner_1ToOFF,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    await air_conditioner_2.add_method(
        ua.NodeId('air_conditioner_2/switch_on', idx),
        'switch_on',
        air_conditioner_2ToON,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    await air_conditioner_2.add_method(
        ua.NodeId('air_conditioner_2/switch_off', idx),
        'switch_off',
        air_conditioner_2ToOFF,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    await air_conditioner_3.add_method(
        ua.NodeId('air_conditioner_3/switch_on', idx),
        'switch_on',
        air_conditioner_3ToON,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    await air_conditioner_3.add_method(
        ua.NodeId('air_conditioner_3/switch_off', idx),
        'switch_off',
        air_conditioner_3ToOFF,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )

    _logger.info(f'Starting server!')

    
    async with server:
        while True:
            await asyncio.sleep(2)



if __name__ == '__main__':
    asyncio.run(main())