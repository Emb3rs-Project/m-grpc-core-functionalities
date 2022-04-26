import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle

from cf.cf_pb2_grpc import CFModuleServicer, add_CFModuleServicer_to_server
from cf.cf_pb2 import PlatformOnlyInput, ConvertSinkOutput, ConvertSourceInput, ConvertSourceOutput, \
    CharacterizationSinkOutput, ConvertOrcOutput, ConvertPinchOutput

from module.Sink.simulation.Convert.convert_sinks import convert_sinks
from module.Source.simulation.Convert.convert_sources import convert_sources

from module.Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from module.Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from module.Sink.characterization.Building.building import building
from module.Sink.characterization.Building.greenhouse import greenhouse
from module.General.Simple_User.simple_user import simple_user

from module.utilities.kb_data import kb

dotenv.load_dotenv()


class CFModule(CFModuleServicer):

    def __init__(self) -> None:
        pass

    def convert_sink(self, request: PlatformOnlyInput, context) -> ConvertSinkOutput:
        in_var = {
            "platform": jsonpickle.decode(request.platform)
        }

        result = convert_sinks(in_var=in_var, kb=kb)
        return ConvertSinkOutput(
            all_sinks_info=jsonpickle.encode(result["all_sinks_info"], unpicklable=True),
            n_demand_list=jsonpickle.encode(result["n_demand_list"], unpicklable=True),
            teo_demand_factor_group=jsonpickle.encode(result["teo_demand_factor_group"], unpicklable=True),
        )

    def convert_source(self, request: ConvertSourceInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
            "gis-module": jsonpickle.decode(request.gis_module),
            "cf-module": jsonpickle.decode(request.cf_module)
        }

        result = convert_sources(in_var=in_var, kb=kb)
        return ConvertSourceOutput(
            all_sources_info=jsonpickle.encode(result['all_sources_info'], unpicklable=True),
            teo_string=jsonpickle.encode(result['teo_string'], unpicklable=True),
            input_fuel=jsonpickle.encode(result['input_fuel'], unpicklable=True),
            output_fuel=jsonpickle.encode(result['output_fuel'], unpicklable=True),
            output=jsonpickle.encode(result['output'], unpicklable=True),
            input=jsonpickle.encode(result['input'], unpicklable=True),
            n_supply_list=jsonpickle.encode(result['n_supply_list'], unpicklable=True),
            teo_capacity_factor_group=jsonpickle.encode(result['teo_capacity_factor_group'], unpicklable=True),
            teo_dhn=jsonpickle.encode(result['teo_dhn'], unpicklable=True),
        )


    def greenhouse(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = greenhouse(in_var=in_var)
        return CharacterizationSinkOutput(
            hot_stream=jsonpickle.encode(result['hot_stream'], unpicklable=True),
        )

    def building(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = building(in_var=in_var,kb=kb)
        return CharacterizationSinkOutput(
            hot_stream=jsonpickle.encode(result['hot_stream'], unpicklable=True),
            cold_stream=jsonpickle.encode(result['cold_stream'], unpicklable=True),
        )

    def convert_orc(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = convert_orc(in_var=in_var,kb=kb)
        return ConvertOrcOutput(
            best_options=jsonpickle.encode(result['best_options'], unpicklable=True),
        )

    def convert_pinch(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = convert_pinch(in_var=in_var,kb=kb)
        return ConvertPinchOutput(
            co2_optimization=jsonpickle.encode(result['co2_optimization'], unpicklable=True),
            energy_recovered_optimization=jsonpickle.encode(result['energy_recovered_optimization'], unpicklable=True),
            energy_investment_optimization=jsonpickle.encode(result['energy_investment_optimization'], unpicklable=True),
        )

    def simple_user(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = simple_user(in_var=in_var)
        return ConvertPinchOutput(
            streams=jsonpickle.encode(result['streams'], unpicklable=True),
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CFModuleServicer_to_server(CFModule(), server)

    server.add_insecure_port(f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    print(f"CF module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
