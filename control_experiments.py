from sacred import Experiment

import subprocess
import sys
import re

from utils import read_args, form_parameters_dict, get_model_subpath

ex = Experiment('my_experiment')

@ex.config
def my_config():
    skip_testing = 0
    reload = 0
    max_epochs = 50

    dynet_gpu = 0

    host="localhost"
    experiment_name = "default_experiment_name"

    lang_name = "turkish"

    datasets_root = "/home/onur/projects/research/turkish-ner/datasets"

    learning_rate = 0.01

    crf = 1
    # lr_method = "sgd-learning_rate_float@%lf" % learning_rate
    lr_method = "adam"

    batch_size = 1

    sparse_updates_enabled = 1
    dropout = 0.5
    char_dim = 64
    char_lstm_dim = 64

    morpho_tag_dim = 64
    morpho_tag_lstm_dim = 64
    morpho_tag_type = "char"

    morpho_tag_column_index = 1

    integration_mode = 0
    active_models = 0
    multilayer = 0
    shortcut_connections = 0

    word_dim = 64
    word_lstm_dim = 64
    cap_dim = 0

    # char_dim = 200
    # char_lstm_dim = 200
    #
    # morpho_tag_dim = 100
    # morpho_tag_lstm_dim = 200
    # morpho_tag_type = "wo_root"
    #
    # morpho_tag_column_index = 1
    #
    # integration_mode = 0
    #
    # word_dim = 300
    # word_lstm_dim = 200
    # cap_dim = 100

    file_format = "conllu"

    debug = 0

    ner_train_file = ""
    ner_dev_file = ""
    ner_test_file = ""

    md_train_file = ""
    md_dev_file = ""
    md_test_file = ""

    use_golden_morpho_analysis_in_word_representation = 0

    embeddings_filepath = "turkish/we-300.txt"


@ex.main
def my_main():

    train_a_single_configuration()


@ex.capture
def train_a_single_configuration(
        lang_name,
        datasets_root,
        crf,
        lr_method,
        batch_size,
        sparse_updates_enabled,
        dropout,
        char_dim,
        char_lstm_dim,
        morpho_tag_dim,
        morpho_tag_lstm_dim,
        morpho_tag_type,
        morpho_tag_column_index,
        word_dim,
        word_lstm_dim,
        cap_dim, skip_testing, max_epochs,
        file_format,
        debug,
        ner_train_file,
        ner_dev_file,
        ner_test_file,
        md_train_file,
        md_dev_file,
        md_test_file,
        use_golden_morpho_analysis_in_word_representation,
        embeddings_filepath,
        integration_mode,
        active_models,
        multilayer,
        shortcut_connections,
        reload,
        dynet_gpu,
        _run):

    """
    python train.py --pre_emb ../../data/we-300.txt --train dataset/gungor.ner.train.only_consistent --dev dataset/gungor.ner.dev.only_consistent --test dataset/gungor.ner.test.only_consistent --word_di
m 300  --word_lstm_dim 200 --word_bidirect 1 --cap_dim 100 --crf 1 --lr_method=sgd-learning_rate_float@0.05 --maximum-epochs 50 --char_dim 200 --char_lstm_dim 200 --char_bid
irect 1 --overwrite-mappings 1 --batch-size 1 --morpho_tag_dim 100 --integration_mode 2
    """

    execution_part = "python main.py --command train --overwrite-mappings 1 "

    if sparse_updates_enabled == 0:
        execution_part += "--disable_sparse_updates "

    if dynet_gpu == 1:
        execution_part += "--dynet-gpu 1 "

    if use_golden_morpho_analysis_in_word_representation == 1:
        execution_part += "--use_golden_morpho_analysis_in_word_representation "

    execution_part += "--debug " + str(debug) + " "

    if word_dim == 0:
        embeddings_part = ""
    else:
        if embeddings_filepath:
            embeddings_part = "--pre_emb %s/%s " % (datasets_root, embeddings_filepath)
        else:
            embeddings_part = ""

    always_constant_part = "--lang_name %s --file_format %s " \
                           "--ner_train_file %s/%s/%s " \
                           "%s" \
                           "--ner_test_file %s/%s/%s " \
                           "--md_train_file %s/%s/%s " \
                           "%s" \
                           "--md_test_file %s/%s/%s " \
                           "%s" \
                           "--skip-testing %d " \
                           "--tag_scheme iobes " \
                           "--maximum-epochs %d " % (lang_name, file_format,
                                                     datasets_root, lang_name, ner_train_file,
                                                     ("--ner_dev_file %s/%s/%s " % (datasets_root, lang_name, ner_dev_file)) if ner_dev_file else "",
                                                     datasets_root, lang_name, ner_test_file,
                                                     datasets_root, lang_name, md_train_file,
                                                     ("--md_dev_file %s/%s/%s " % (datasets_root, lang_name,
                                                                                    md_dev_file)) if md_dev_file else "",
                                                     datasets_root, lang_name, md_test_file,
                                                     embeddings_part,
                                                     skip_testing, max_epochs)

    commandline_args = always_constant_part + \
              "--crf %d " \
              "--lr_method %s " \
              "--batch-size %d " \
              "--dropout %1.1lf " \
              "--char_dim %d " \
              "--char_lstm_dim %d " \
              "--morpho_tag_dim %d " \
              "--morpho_tag_lstm_dim %d " \
              "--morpho_tag_type %s " \
              "--morpho-tag-column-index %d " \
              "--word_dim %d " \
              "--word_lstm_dim %d "\
              "--cap_dim %d "\
              "--integration_mode %d " \
              "--active_models %d " \
              "--multilayer %d " \
              "--shortcut_connections %d " \
              "--reload %d" % (crf,
                               lr_method,
                               batch_size,
                               dropout,
                               char_dim,
                               char_lstm_dim,
                               morpho_tag_dim,
                               morpho_tag_lstm_dim,
                               morpho_tag_type,
                               morpho_tag_column_index,
                               word_dim,
                               word_lstm_dim,
                               cap_dim,
                               integration_mode,
                               active_models,
                               multilayer,
                               shortcut_connections,
                               reload)

    # tagger_root = "/media/storage/genie/turkish-ner/code/tagger"

    print _run
    print _run.info

    print subprocess.check_output(["id"])
    print subprocess.check_output(["pwd"])

    opts = read_args(args_as_a_list=commandline_args.split(" "))
    print opts
    parameters = form_parameters_dict(opts)
    print parameters
    # model_path = get_name(parameters)
    model_path = get_model_subpath(parameters)
    print model_path

    task_names = ["NER", "MORPH"]

    for task_name in task_names:
        _run.info["%s_dev_f_score" % task_name] = dict()
        _run.info["%s_test_f_score" % task_name] = dict()

    _run.info['starting'] = 1

    dummy_prefix = ""

    full_commandline = dummy_prefix + execution_part + commandline_args

    print full_commandline
    process = subprocess.Popen(full_commandline.split(" "),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    def record_metric(epoch, label, value):
        epoch_str = str(epoch)
        if epoch_str in _run.info[label]:
            _run.info[label][epoch_str].append(value)
        else:
            _run.info[label][epoch_str] = [value]

    def capture_information(line):

        # 1
        """
        NER Epoch: %d Best dev and accompanying test score, best_dev, best_test: %lf %lf 
        """
        for task_name in task_names:
            m = re.match("^%s Epoch: (\d+) .* best_dev, best_test: (.+) (.+)$" % task_name, line)
            if m:
                epoch = int(m.group(1))
                best_dev = float(m.group(2))
                best_test = float(m.group(3))

                record_metric(epoch, "%s_dev_f_score" % task_name, best_dev)
                record_metric(epoch, "%s_test_f_score" % task_name, best_test)

    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        capture_information(line)
        sys.stdout.flush()

    return model_path


if __name__ == '__main__':
    ex.run_commandline()