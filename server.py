import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle
import json

from cf.cf_pb2_grpc import CFModuleServicer, add_CFModuleServicer_to_server
from cf.cf_pb2 import CharacterizationInput, CharacterizationOutput, CharacterizationSourceOutput, PlatformOnlyInput, ConvertSinkOutput, ConvertSourceInput, ConvertSourceOutput, \
    CharacterizationSinkOutput, ConvertOrcOutput, ConvertPinchOutput
from module.Sink.characterization.building_adjust_capacity import building_adjust_capacity

from module.Sink.simulation.convert_sinks import convert_sinks
from module.Source.simulation.Convert.convert_sources import convert_sources

from module.Source.simulation.Heat_Recovery.ORC.convert_orc import convert_orc
from module.Source.simulation.Heat_Recovery.Pinch.convert_pinch import convert_pinch
from module.Sink.characterization.building import building
from module.Sink.characterization.greenhouse import greenhouse
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
            all_sinks_info=json.dumps(
                result["all_sinks_info"]),
            n_demand_list=json.dumps(
                result["n_demand_list"]),
            teo_demand_factor_group=json.dumps(
                result["teo_demand_factor_group"]),
        )

    def convert_source(self, request: ConvertSourceInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
            "gis_module": jsonpickle.decode(request.gis_module),
            "cf_module": jsonpickle.decode(request.cf_module)
        }

        result = convert_sources(in_var=in_var, kb=kb)
        return ConvertSourceOutput(
            all_sources_info=json.dumps(
                result['all_sources_info']),
            teo_string=json.dumps(
                result['teo_string']),
            input_fuel=json.dumps(
                result['input_fuel']),
            output_fuel=json.dumps(
                result['output_fuel']),
            output=json.dumps(result['output']),
            input=json.dumps(result['input']),
            n_supply_list=json.dumps(
                result['n_supply_list']),
            teo_capacity_factor_group=json.dumps(
                result['teo_capacity_factor_group']),
            teo_dhn=json.dumps(result['teo_dhn']),
        )

    def char_greenhouse(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = greenhouse(in_var=in_var)
        return CharacterizationSinkOutput(
            hot_stream=json.dumps(
                result['hot_stream']),
        )

    def char_building(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = building(in_var=in_var, kb=kb)
        return CharacterizationSinkOutput(
            hot_stream=json.dumps(result['hot_stream']),
            cold_stream=json.dumps(result['cold_stream']),
        )

    def convert_orc(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = convert_orc(in_var=in_var, kb=kb)
        return ConvertOrcOutput(
            best_options=json.dumps(result['best_options']),
            report=result['report']
        )

    def convert_pinch(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = convert_pinch(in_var=in_var, kb=kb)
        return ConvertPinchOutput(
            co2_optimization=json.dumps(result['co2_optimization']),
            energy_recovered_optimization=json.dumps(
                result['energy_recovered_optimization']),
            energy_investment_optimization=json.dumps(
                result['energy_investment_optimization']),
        )

    def char_simple(self, request: PlatformOnlyInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform),
        }
        result = simple_user(in_var=in_var)
        return CharacterizationSourceOutput(
            streams=json.dumps(result['streams']),
        )

    def char_adjust_capacity(self, request: CharacterizationInput, context):
        in_var = {
            "platform": jsonpickle.decode(request.platform)
        }
        result = building_adjust_capacity(in_var=in_var)
        return CharacterizationOutput(
            stream=json.dumps(result)
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CFModuleServicer_to_server(CFModule(), server)

    server.add_insecure_port(
        f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    print(
        f"CF module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


serve()