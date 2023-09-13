import logging
import asyncio
import sys
import psutil
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
def echo(parent, string1, string2):
    print(string1 + ' ' + string2)
    return string1 + ' ' + string2


async def main():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/opcua_server/')
    server.set_server_name("Kaixo MUndua OPCUA")

    # setup our own namespace
    uri = 'http://examples.mondragon.edu/opcua'
    idx = await server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.nodes.objects

    # populating our address space with an object
    myobj = await objects.add_object(
        ua.NodeId('https://mondragon.edu/object/computer', 2),
        'Computer'
    )

    # Read only variables
    cpu = await myobj.add_variable(
        ua.NodeId('https://mondragon.edu/object/computer/cpu_percent', 2),
        'cpu_percent',
        psutil.cpu_percent()
    )
    ram = await myobj.add_variable(
        ua.NodeId('https://mondragon.edu/object/computer/ram_percent', 2),
        'ram_percent',
        psutil.virtual_memory().percent
    )
    battery = await myobj.add_variable(
        ua.NodeId('https://mondragon.edu/object/computer/battery_percent', 2),
        'battery_percent',
        psutil.sensors_battery().percent
    )

    # Writable variables
    myvar = await myobj.add_variable(
        ua.NodeId('https://mondragon.edu/object/computer/write_me', 2),
        'WriteMe',
        6.7
    )
    await myvar.set_writable()

    # Add a method
    await objects.add_method(
        ua.NodeId('https://mondragon.edu/methods/echo', 2),
        ua.QualifiedName('Echo', 2),
        echo,
        [ua.VariantType.String],
        [ua.VariantType.String],
        [ua.VariantType.String]
    )
    _logger.info(f'Starting server!')

    # Update values
    async with server:
        while True:
            await asyncio.sleep(1)

            new_cpu = psutil.cpu_percent()
            await cpu.write_value(new_cpu)

            new_ram = psutil.virtual_memory().percent
            await ram.write_value(new_ram)

            new_battery = psutil.sensors_battery().percent
            await battery.write_value(new_battery)

if __name__ == '__main__':
    asyncio.run(main())