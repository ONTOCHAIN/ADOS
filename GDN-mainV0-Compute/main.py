# -*- coding: utf-8 -*-
#import pdb # Para hacer debug, donde queramos parar se inserta pdb.set_trace()
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, random_split, Subset

from sklearn.preprocessing import MinMaxScaler

from util.env import get_device, set_device
from util.preprocess import build_loc_net, construct_data
from util.net_struct import get_feature_map, get_fc_graph_struc
from util.iostream import printsep

from datasets.TimeDataset import TimeDataset

from models.GDN import GDN

#from train import train
from test  import test
#from evaluate import get_err_scores, get_best_performance_data, get_val_performance_data, get_full_err_scores

import sys
from datetime import datetime

import os
import argparse
from pathlib import Path

import matplotlib.pyplot as plt

import json
import random




class Main():
    def __init__(self, train_config, env_config, debug=False):

        print('>>> main.py # Inicio de Constructor <<<')

        self.train_config = train_config
        self.env_config = env_config
        self.datestr = None

        dataset = self.env_config['dataset'] 

######  DATOS DE LA CARPETA MSL    
        #train_orig = pd.read_csv(f'{dataset}/train.csv', sep=',', index_col=0)
        #archivo de entrada para el modelo
        test_orig = pd.read_csv(f'{dataset}/test.csv', sep=',', index_col=0)

######  DATOS DE LA CARPETA swat_demo
#        train_orig = pd.read_csv(f'{dataset}/swat_train_demo.csv', sep=',', index_col=0)
#        test_orig = pd.read_csv(f'{dataset}/swat_test_demo.csv', sep=',', index_col=0)
        
######  DATOS DE LA CARPETA swamo
#        train_orig = pd.read_csv(f'{dataset}/train.csv', sep=',', index_col=0)
#        test_orig = pd.read_csv(f'{dataset}/test.csv', sep=',', index_col=0)

######  DATOS DE LA CARPETA swat_demo
#        train_orig = pd.read_csv(f'{dataset}/wadi_train_demo.csv', sep=',', index_col=0)
#        test_orig = pd.read_csv(f'{dataset}/wadi_test_demo.csv', sep=',', index_col=0)        

        #train, test = train_orig, test_orig
        test = test_orig
        #print('tamaño original train')
        #print(len(train))
        print('tamaño original test')
        print(len(test))
        if 'attack' in test.columns:
            train = test.drop(columns=['attack'])
        else: 
            train=test
            
        #if 'attack' in train.columns:
        #    train = train.drop(columns=['attack'])

        feature_map = get_feature_map(dataset)
        fc_struc = get_fc_graph_struc(dataset)

        set_device(env_config['device'])
        self.device = get_device()

        fc_edge_index = build_loc_net(fc_struc, list(train.columns), feature_map=feature_map)
        fc_edge_index = torch.tensor(fc_edge_index, dtype = torch.long)
        print(train.columns)
        print(test.columns)

        self.feature_map = feature_map
        print('tamaño feature map')
        print(len(feature_map))
        
        #train_dataset_indata = construct_data(train, feature_map, labels=0)
        test_dataset_indata = construct_data(test, feature_map, labels=test.attack.tolist())

        # slide win es la ventana que va cogiendo de datos (en las pruebas ponemos =5
        #y entonces al hacer TImeDataSet se queda con un tamaño menos 5 al original.
        # slide stride es el step q hace
        cfg = {
            'slide_win': train_config['slide_win'],
            'slide_stride': train_config['slide_stride'],
        }

        
        #train_dataset = TimeDataset(train_dataset_indata, fc_edge_index, mode='train', config=cfg)
        test_dataset = TimeDataset(test_dataset_indata, fc_edge_index, mode='test', config=cfg)

        print('tamaño TimedataSet de test')
        print(len(test_dataset))


        self.test_dataset = test_dataset
        
        
        self.test_dataloader = DataLoader(test_dataset, batch_size=train_config['batch'],
                            shuffle=False, num_workers=0)
        
        print('tamaño dataLoader de test')
        print(len(self.test_dataloader))
        
        edge_index_sets = []
        edge_index_sets.append(fc_edge_index)

        self.model = GDN(edge_index_sets, len(feature_map), 
                dim=train_config['dim'], 
                input_dim=train_config['slide_win'],
                out_layer_num=train_config['out_layer_num'],
                out_layer_inter_dim=train_config['out_layer_inter_dim'],
                topk=train_config['topk']
            ).to(self.device)

    def run(self):
        
        print('>>> main.py # Inicio de run() <<<')

        if len(self.env_config['load_model_path']) > 0:
            model_save_path = self.env_config['load_model_path']
        else:
            model_save_path = self.get_save_path()[0]

        print('>>> main.py # Imprimimos  model_save_path <<<')
        print(model_save_path)
        #print(self.env_config['load_model_path'])
        
        # test
        #para cargar el modelo que ha sido entrenado

        print('>>> main.py # load_state_dict <<<')
        self.model.load_state_dict(torch.load(model_save_path))
        best_model = self.model.to(self.device)
        print('>>> main.py # test_result <<<')
        _, self.test_result = test(best_model, self.test_dataloader)
        #print(self.test_result)
        #seguir por aquí
        print(len(self.test_result[2:][0][0:]))
        print(self.test_result)
        
        #print('>>> main.py # val_result <<<')
        #_, self.val_result = test(best_model, self.val_dataloader)


        # save result for iexec
        #with open(os.path.join(output_directory, "result.json"), 'w+') as f:
        #    json.dump(result, f)
        # este parece q es necesario
        #with open(os.path.join(output_directory, "computed.json"), 'w+') as f:
        #    json.dump(
        #        {"deterministic-output-path": os.path.join(output_directory, "result.json")}, f)

        dir_path = self.env_config['save_path'] 
        df = pd.DataFrame(self.test_result[2:][0][0:])
        df.to_csv(f'{dir_path}/output.csv')


    def get_save_path(self, feature_name=''):

        dir_path = self.env_config['save_path']
        print(dir_path)
        
        if self.datestr is None:
            now = datetime.now()
            self.datestr = now.strftime('%m|%d-%H:%M:%S')
        datestr = self.datestr          

        paths = [
            f'{dir_path}/pretrained/best_{datestr}.pt',
            f'{dir_path}/results/{datestr}.csv',
        ]

        for path in paths:
            dirname = os.path.dirname(path)
            Path(dirname).mkdir(parents=True, exist_ok=True)

        return paths

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-batch', help='batch size', type = int, default=128)
    parser.add_argument('-epoch', help='train epoch', type = int, default=100)
    parser.add_argument('-slide_win', help='slide_win', type = int, default=15)
    parser.add_argument('-dim', help='dimension', type = int, default=64)
    parser.add_argument('-slide_stride', help='slide_stride', type = int, default=5)
    parser.add_argument('-save_path_pattern', help='save path pattern', type = str, default='')
    parser.add_argument('-dataset', help='wadi / swat', type = str, default='wadi')
    parser.add_argument('-device', help='cuda / cpu', type = str, default='cuda')
    parser.add_argument('-random_seed', help='random seed', type = int, default=0)
    parser.add_argument('-comment', help='experiment comment', type = str, default='')
    parser.add_argument('-out_layer_num', help='outlayer num', type = int, default=1)
    parser.add_argument('-out_layer_inter_dim', help='out_layer_inter_dim', type = int, default=256)
    parser.add_argument('-decay', help='decay', type = float, default=0)
    parser.add_argument('-val_ratio', help='val ratio', type = float, default=0.1)
    parser.add_argument('-topk', help='topk num', type = int, default=20)
    parser.add_argument('-report', help='best / val', type = str, default='best')
    parser.add_argument('-load_model_path', help='trained model path', type = str, default='')

    args = parser.parse_args()

    random.seed(args.random_seed)
    np.random.seed(args.random_seed)
    torch.manual_seed(args.random_seed)
    torch.cuda.manual_seed(args.random_seed)
    torch.cuda.manual_seed_all(args.random_seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    os.environ['PYTHONHASHSEED'] = str(args.random_seed)

    #for iexec
    #input_directory = os.environ['IEXEC_IN']
    #output_directory = os.environ['IEXEC_OUT']
    #input_filename = os.environ['IEXEC_DATASET_FILENAME']

    train_config = {
        'batch': args.batch,
        'epoch': args.epoch,
        'slide_win': args.slide_win,
        'dim': args.dim,
        'slide_stride': args.slide_stride,
        'comment': args.comment,
        'seed': args.random_seed,
        'out_layer_num': args.out_layer_num,
        'out_layer_inter_dim': args.out_layer_inter_dim,
        'decay': args.decay,
        'val_ratio': args.val_ratio,
        'topk': args.topk,
    }

    env_config={
        'save_path': args.save_path_pattern,
        'dataset': args.dataset,
        'report': args.report,
        'device': args.device,
        'load_model_path': args.load_model_path
    }

    main = Main(train_config, env_config, debug=False)
    main.run()

