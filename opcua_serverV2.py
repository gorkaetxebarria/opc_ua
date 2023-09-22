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
    async def move_left(parent):
        time.sleep(5)
        await state.write_value("Rest position")
        return 'Move to left completed'
    @uamethod
    async def move_right(parent):
        time.sleep(5)
        await state.write_value('Piece Placed')
        return 'Move to right completed'
    @uamethod
    async def reset(parent):
        time.sleep(5)
        await state.write_value('Reset')
        return 'Reset'
    
    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects
    # Create object
    robotic_arm = await objects.add_object(
        ua.NodeId('robotic_arm', idx),
        'Robotic Arm'
    )

    temp = await robotic_arm.add_variable(
        ua.NodeId('roboticarm/temperature', idx),
        'temperature',
        0
    )
    spd = await robotic_arm.add_variable(
        ua.NodeId('robotic_arm/speed', idx),
        'speed',
        0
    )

    state = await robotic_arm.add_variable(
        ua.NodeId('robotic_arm/state', idx),
        'state',
        ''
    )

    # Add methods
    await robotic_arm.add_method(
        ua.NodeId('robotic_arm/move_left', idx),
        'move_left',
        move_left,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )

    await robotic_arm.add_method(
        ua.NodeId('robotic_arm/move_right', idx),
        'move_right',
        move_right,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    
    await robotic_arm.add_method(
        ua.NodeId('robotic_arm/reset', idx),
        'reset',
        reset,
        [ua.VariantType.NodeId],
        [ua.VariantType.String]
    )
    _logger.info(f'Starting server!')

    
    async with server:
        while True:
            await asyncio.sleep(2)
            temperature = random.randint(30, 60)
            speed = random.randint(20, 60)

            await temp.write_value(temperature)
            await spd.write_value(speed)
            print('temp: ' + str(temperature) + ' and speed: ' + str(speed))



if __name__ == '__main__':
    asyncio.run(main())