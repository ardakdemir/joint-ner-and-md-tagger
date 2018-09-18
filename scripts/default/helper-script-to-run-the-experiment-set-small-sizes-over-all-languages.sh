#!/usr/bin/env bash

experiment_name=${1:-section1-all-20171114-08}
original_experiment_name=${experiment_name}

virtualenvwrapper_path=`which virtualenvwrapper.sh`

configuration_variables_path=${2:-./scripts/default/configuration-variables.sh}

if [ -f ${configuration_variables_path} ]; then
    source ${configuration_variables_path};
fi

ner_tagger_root=${ner_tagger_root:-~/projectdir}
virtualenv_name=${virtualenv_name:-virtualenv_containing_dynet}
datasets_root=~/Desktop/projects/research/datasets/
experiment_logs_path=`pwd`/experiment-logs/
file_format=conllu

if [ ! -d ${experiment_logs_path} ]; then
    mkdir ${experiment_logs_path};
fi

environment_variables_path=environment-variables

#sacred_args='-m localhost:17017:joint_ner_and_md'
sacred_args='-F '${experiment_logs_path}

preamble="cd ${ner_tagger_root} && \
          source ${virtualenvwrapper_path} && \
          workon ${virtualenv_name} && \
          source ${environment_variables_path} && \
          python control_experiments.py ${sacred_args} with "

n_trials=10

dim=10
morpho_tag_type=char

for trial in `seq 1 ${n_trials}`; do

    for lang_name in czech spanish finnish hungarian; do

        lang_dataset_root=${datasets_root}/${lang_name}

        ini_filepath=${lang_dataset_root}/${lang_name}-joint-md-and-ner-tagger.ini
        lang_dataset_filepaths=`python ./utils/ini_parse.py --input ${ini_filepath} --query ner.train_file ner.dev_file ner.test_file md.train_file md.dev_file md.test_file`

        # lang_dataset_root=${lang_dataset_root}
        dataset_filepaths="file_format=${file_format} lang_name=${lang_name} datasets_root=${datasets_root} ${lang_dataset_filepaths} "

        for morpho_tag_type in char ; do

            small_sizes="char_dim=$dim \
            char_lstm_dim=$dim \
            morpho_tag_dim=$dim \
            morpho_tag_lstm_dim=$dim \
            morpho_tag_type=${morpho_tag_type} \
            word_dim=$dim \
            word_lstm_dim=$dim \
            lr_method=sgd-learning_rate_float@0.01 "

            # experiment_name=${original_experiment_name}-dim-${dim}-morpho_tag_type-${morpho_tag_type}-trial-`printf "%02d" ${trial}`
            experiment_name=${original_experiment_name}-dim-${dim}-morpho_tag_type-${morpho_tag_type}-lang_name-${lang_name}

            pre_command="echo ${original_experiment_name}-dim-${dim}-morpho_tag_type-${morpho_tag_type}-lang_name-${lang_name}-trial-`printf "%02d" ${trial}` >> ${experiment_name}.log"

            for imode in 0 1 2 ; do
                if [[ $imode == 0 ]]; then
                    for amodels in 1 0 ; do
                        command=${pre_command}" && "" ${preamble} \
                        active_models=${amodels} \
                        integration_mode=$imode \
                        dynet_gpu=0 \
                        embeddings_filepath=\"\" \
                        ${dataset_filepaths} \
                        $small_sizes \
                        experiment_name=${experiment_name} ;"
                        echo $command;
                    done;
                    command=${pre_command}" && "" ${preamble} \
                    active_models=0 \
                    integration_mode=0 \
                    use_golden_morpho_analysis_in_word_representation=1 \
                    dynet_gpu=0 \
                    embeddings_filepath=\"\" \
                    ${dataset_filepaths} \
                    $small_sizes \
                    experiment_name=${experiment_name} ;"
                    echo $command;
                elif [[ $imode == 1 ]]; then
                    command=${pre_command}" && "" ${preamble} \
                    active_models=2 \
                    integration_mode=1 \
                    dynet_gpu=0 \
                    embeddings_filepath=\"\" \
                    ${dataset_filepaths} \
                    $small_sizes \
                    experiment_name=${experiment_name} ;"
                    echo $command;
                else
                    command=${pre_command}" && "" ${preamble} \
                    active_models=2 \
                    integration_mode=2 \
                    multilayer=1 \
                    shortcut_connections=1 \
                    dynet_gpu=0 \
                    embeddings_filepath=\"\" \
                    ${dataset_filepaths} \
                    $small_sizes \
                    experiment_name=${experiment_name} ;"
                    echo $command;

                    command=${pre_command}" && "" ${preamble} \
                    active_models=2 \
                    integration_mode=2 \
                    dynet_gpu=0 \
                    embeddings_filepath="" \
                    ${dataset_filepaths} \
                    $small_sizes \
                    experiment_name=${experiment_name} ;"
                    echo $command;

                fi ;
            done

        done

	done
done