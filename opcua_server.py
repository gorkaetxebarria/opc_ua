import logging
import asyncio
import sys
import psutil
import random
import time
sys.path.insert(0, "..")


from asyncua import Server, ua
from asyncua.common.methods import uamethod

# Configure logger
logging.basicConfig(
    format=f'%(asctime)s %(levelname)-8s: %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
_logger = logging.getLogger('asyncua')


@uamethod
def update_temperature_and_speed(parent):
    temperature = random.randint(30, 60)
    speed = random.randint(20, 40)

    parent.write_value('temperature', temperature)
    parent.write_value('speed', speed)

    return 'temperature: '+ temperature +"  speed: " + speed


@uamethod
def moveLeft(parent):
    parent.state = 'Rest position'
    time.sleep(5)
    return 'Move to left completed'


@uamethod
def moveRight(parent):
    parent.state = 'Piece placed'
    time.sleep(5)
    return 'Move to right completed'



async def main():
    states = ['Rest position', 'Piece Placed']
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/opcua_server/')
    server.set_server_name("Kaixo MUndua OPCUA")

    # setup our own namespace
    uri = 'http://examples.mondragon.edu/opcua'
    idx = await server.register_namespace(uri)
    

    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects
    # Create object
    robotic_arm = await objects.add_object(
        ua.NodeId('https://mondragon.edu/object/robotic_arm', 2),
        'Robotic Arm'
    )
    

    temp=await robotic_arm.add_variable(
        ua.NodeId('https://mondragon.edu/object/robotic_arm/temperature',2),
        'temperature',
        0
    )
    spd=await robotic_arm.add_variable(
        ua.NodeId('https://mondragon.edu/object/robotic_arm/speed',2),
        'speed',
        0
    )
    
    state= await robotic_arm.add_variable(
        ua.NodeId('https://mondragon.edu/object/robotic_arm/state', 2),
        'state',
        states
    )

    # Add a method
    await objects.add_method(
        ua.NodeId('2:UpdateTemperatureAndSpeed', idx),
        ua.QualifiedName('UpdateTemperatureAndSpeed', idx),
        update_temperature_and_speed,
        [ua.VariantType.String]
    )


    await objects.add_method(
    ua.NodeId(
        '2:MoveLeft',  # Use the namespace index and method name
        idx  # Specify the namespace index you previously registered
    ),
    ua.QualifiedName('MoveLeft', idx),  # Use the same namespace index
    moveLeft,
    [ua.VariantType.String]
)

    await objects.add_method(
    ua.NodeId(
        '2:MoveRight',  # Use the namespace index and method name
        idx  # Specify the namespace index you previously registered
    ),
    ua.QualifiedName('MoveRight', idx),  # Use the same namespace index
    moveRight,
    [ua.VariantType.String]
)

    _logger.info(f'Starting server!')

    # Start server
    server.start()

    # Loop to update temperature and speed
    try:
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()


if __name__ == '__main__':
    asyncio.run(main())