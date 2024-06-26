import os
import sys
import yaml
import traceback

root_dir_path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(os.path.join(root_dir_path, 'src'))

user_inputs_dir = os.path.join(root_dir_path, 'user_run_files')
from scripts.script_generate_with_new_architecture import generate_with_new_architecture
from scripts.param_id_run_script import run_param_id
from scripts.plot_param_id_script import plot_param_id

if __name__ == '__main__':
    try:
        with open(os.path.join(user_inputs_dir, 'user_inputs.yaml'), 'r') as file:
            inp_data_dict = yaml.load(file, Loader=yaml.FullLoader)

        print('_________Running all param_id tests_____________')
        print('')

        # print('running 3compartment autogeneration test')
        # inp_data_dict['file_prefix'] = '3compartment'
        # inp_data_dict['input_param_file'] = '3compartment_parameters.csv'

        # generate_with_new_architecture(False, inp_data_dict)
        if 'resources_dir' in inp_data_dict.keys():
            # remove that entry so it doesnt get passed to the param_id script
            # so the default dirs are used
            del inp_data_dict['resources_dir']
        if 'generated_model_dir' in inp_data_dict.keys():
            del inp_data_dict['generated_model_dir']
        if 'param_id_output_dir' in inp_data_dict.keys():
            del inp_data_dict['param_id_output_dir']

        print('')
        print('running simple_physiological parameter id test')
        inp_data_dict['file_prefix'] = 'simple_physiological'
        inp_data_dict['input_param_file'] = 'simple_physiological_parameters.csv'
        inp_data_dict['param_id_method'] = 'genetic_algorithm'
        inp_data_dict['pre_time'] = 20
        inp_data_dict['sim_time'] = 2
        inp_data_dict['maximum_step'] = 0.001
        inp_data_dict['dt'] = 0.01
        inp_data_dict['DEBUG'] = True
        inp_data_dict['param_id_obs_path'] = os.path.join(root_dir_path,'resources/simple_physiological_obs_data.json')
        inp_data_dict['do_mcmc'] = True
        inp_data_dict['debug_ga_options']['num_calls_to_function'] = 60
        run_param_id(inp_data_dict)

        # also test running autogeneration with the fit parameters
        generate_with_new_architecture(True, inp_data_dict)

        # also test plotting
        plot_param_id(inp_data_dict)

        # TODO More tests here. Probably sympathetic neuron!!
        # And maybe the lung_ROM to test the frequency domian fitting

        print('param ID tests complete. TODO add more param id tests to test',
              'all functionality')

    except:
        print(traceback.format_exc())
        exit()
