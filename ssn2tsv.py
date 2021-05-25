#! /usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################################################
##########################################################################################
##
##                                Library
##
##########################################################################################
##########################################################################################

import argparse
from textwrap import dedent
import sys, os
import re 

##########################################################################################
##########################################################################################
##
##                                Function
##
##########################################################################################
##########################################################################################

def clean_tsv(output, tmp, header_order):
    '''
    Second step of the full table to be sure that if a node have more item than the first one
    it will create a table with all the informations for each line (add the new item to the header
    and give extra blank item to the columns without)

    :param output: name of the output final file
    :type: str
    :param tmp: name of the tmp file that will be remove at this step
    :type: str
    :param header_order: final name of the header with all the columns that appread of the ssn
    :type: list of str
    :return: nothing
    '''

    num_items_header = len(header_order)
    header = True

    with open(tmp, 'r') as r_file :
        with open(output, 'w') as w_file :
            for line in r_file :
                line_rstrip = line.rstrip('\n')
                line2list = line_rstrip.split('\t')

                num_items = len(line2list)

                if num_items != num_items_header :
                    if header :
                        w_file.write('\t'.join(header_order) + '\n')
                        header = False
                    else :
                        to_add = num_items_header - num_items

                        line_rstrip += '\t' * to_add
                        w_file.write(line_rstrip + '\n')
                else :
                    w_file.write(line)
    os.remove(tmp)

    return

##########################################################################################
##########################################################################################

def xgmml2tsv_full(xgmml, output) :
    '''
    Function that read the xgmml line by line and create the tsv in the same time

    :param xgmml: the SNN in xgmml format
    :type: str
    :param output: Name of the output tsv file
    :type: str
    '''

    dict_columns = {}

    header = True
    header_order = []
    node = False

    value_re = re.compile('[vl]a[bl][eu][el]="([^"]+)')
    name_re = re.compile('name="([^"]+)')

    with open(xgmml, 'r') as g_file :
        with open('tmp.tsv', 'w') as w_file :
            for line in g_file:
                if '</node>' in line :
                    node = False 

                    x = ''

                    for header_name in header_order :
                        if 'Cluster IDs' in header_name:
                            x = header_name

                    if "List of IDs in Rep Node" not in header_order and x == '' :
                        x = "node id"
                    elif x == '' :
                        x = "List of IDs in Rep Node"

                    num_items = len(dict_columns[x])

                    dict_columns = {item:value if len(value) == num_items else ' -- '.join(value) for item, value in dict_columns.items()}
                    dict_columns = {item:value if '--' not in value else '' for item, value in dict_columns.items()}

                    if header :
                        w_file.write('{}\n'.format('\t'.join(header_order)))
                        header = False
                    else :
                        for index in range(num_items) :
                            line2write = ''

                            for column in header_order :
                                if type(dict_columns[column]) == list :
                                    line2write += '{}\t'.format(dict_columns[column][index])
                                else :
                                    line2write += '{}\t'.format(dict_columns[column])
                            
                            w_file.write(f'{line2write.rstrip()}\n') 

                    dict_columns = {item:[] for item, value in dict_columns.items()}

                elif 'node id' in line :
                    node = True 
                    name = 'node id'
                    value = value_re.search(line).group(1)    

                    if name not in dict_columns :
                        dict_columns[name] = [value]
                    else :
                        dict_columns[name].append(value)

                    if name not in header_order:
                        header_order.append(name)                    

                elif 'list' not in line and '</att>' not in line and node:
                    name = name_re.search(line).group(1)
                    try :
                        value = value_re.search(line).group(1)
                    except AttributeError:
                        value = ''                     

                    if name not in dict_columns :
                        dict_columns[name] = [value]
                    else :
                        dict_columns[name].append(value)

                    if name not in header_order:
                        header_order.append(name)

    clean_tsv(output, 
              'tmp.tsv',
              header_order)

    return



##########################################################################################
##########################################################################################

def xgmml2tsv_taxonomy(xgmml, output) :
    '''
    Function that read the xgmml line by line and create the tsv in the same time

    :param xgmml: the SNN in xgmml format
    :type: str
    :param output: Name of the output tsv file
    :type: str
    '''


    dict_columns = {'Node_id':[],
                    'Cluster_number':[],
                    'Organism':[],
                    'Cluster_color':[],
                    'Description':[],
                    'Taxonomy_ID':[],
                    'Sequence_Length':[],
                    'Gene_Name':[],
                    'Superkingdom':[],
                    'Kingdom':[],
                    'Phylum':[],
                    'Class':[],
                    'Order':[],
                    'Genus':[],
                    'Family':[],
                    'Species':[],
                    'Sequence':[],
                    'UniRef50_IDs':[],
                    'IDs_rep_node':[],
                    "UniRef90_IDs":[]}
    translate_dict = {'node id': 'Node_id',
                          'Sequence Count Cluster Number':'Cluster_number',
                          'Node Count Fill Color':'Cluster_color',
                          'Organism':'Organism',
                          'Taxonomy ID':'Taxonomy_ID',
                          'Description':'Description',
                          'Sequence Length':'Sequence_Length',
                          'Gene Name':'Gene_Name',
                          'Superkingdom':'Superkingdom',
                          'Kingdom':'Kingdom',
                          'Phylum':'Phylum',
                          'Class':'Class',
                          'Order':'Order',
                          'Family':'Family',
                          'Genus':'Genus',
                          'Sequence':'Sequence',
                          'UniRef50 Cluster IDs': "UniRef50_IDs",
                          'UniRef90 Cluster IDs': "UniRef90_IDs",
                          'List of IDs in Rep Node':'IDs_rep_node'}        

    header = True
    header_order = []
    node = False

    value_re = re.compile('[vl]a[bl][eu][el]="([^"]+)')
    name_re = re.compile('name="([^"]+)')

    with open(xgmml, 'r') as g_file :
        with open(output, 'w') as w_file :
            for line in g_file:
                if '</node>' in line :

                    x = ''

                    for header_name in header_order :
                        if '_IDs' in header_name:
                            x = header_name

                    if "IDs_rep_node" not in header_order and x == '' :
                        x = "Node_id"
                    elif x == '' :
                        x = "IDs_rep_node"

                    num_items = len(dict_columns[x])

                    dict_columns = {item:value if len(value) == num_items else ' -- '.join(value) for item, value in dict_columns.items()}
                    dict_columns = {item:value if '--' not in value else '' for item, value in dict_columns.items()}

                    if header :
                        w_file.write('{}\n'.format('\t'.join(header_order)))
                        header = False
                    else :
                        for index in range(num_items) :
                            line2write = ''

                            for column in header_order :
                                if column in dict_columns :
                                    if type(dict_columns[column]) == list :
                                        line2write += '{}\t'.format(dict_columns[column][index])
                                    else :
                                        line2write += '{}\t'.format(dict_columns[column])                      

                            w_file.write(f'{line2write.rstrip()}\n') 

                    dict_columns = {item:[] for item, value in dict_columns.items()}
                    node = False

                elif 'node id' in line :
                    node = True 
                    name = 'node id'
                    value = value_re.search(line).group(1)    

                    if name in translate_dict :
                        new_name = translate_dict[name]

                        if name not in dict_columns :
                            dict_columns[new_name] = [value]
                        else :
                            dict_columns[new_name].append(value)

                        if new_name not in header_order:
                            header_order.append(new_name)                                     

                elif 'list' not in line and '</att>' not in line and node:
                    name = name_re.search(line).group(1)
                    try :
                        value = value_re.search(line).group(1)
                    except AttributeError:
                        value = ''
                
                    if name in translate_dict :
                        new_name = translate_dict[name]

                        if name not in dict_columns :
                            dict_columns[new_name] = [value]
                        else :
                            dict_columns[new_name].append(value)

                        if new_name not in header_order:
                            header_order.append(new_name)
    return

##########################################################################################
##########################################################################################

def xgmml2tsv_default(xgmml, output) :
    '''
    Function that read the xgmml line by line and create the tsv in the same time

    :param xgmml: the SNN in xgmml format
    :type: str
    :param output: Name of the output tsv file
    :type: str
    '''

   
    dict_columns = {'Node_id':[],
                        'Cluster_number':[],
                        'Organism':[],
                        'Cluster_color':[],
                        'Description':[],
                        'Taxonomy_ID':[],
                        'Sequence_Length':[],
                        'Gene_Name':[],
                        'Sequence':[],
                        'UniRef50_IDs':[],
                        'IDs_rep_node':[],
                        "UniRef90_IDs":[]}
    translate_dict = {'node id': 'Node_id',
                          'Sequence Count Cluster Number':'Cluster_number',
                          'Node Count Fill Color':'Cluster_color',
                          'Organism':'Organism',
                          'Taxonomy ID':'Taxonomy_ID',
                          'Description':'Description',
                          'Sequence Length':'Sequence_Length',
                          'Sequence':'Sequence',
                          'UniRef50 Cluster IDs': "UniRef50_IDs",
                          'UniRef90 Cluster IDs': "UniRef90_IDs",
                          'List of IDs in Rep Node':'IDs_rep_node'}

    header = True
    header_order = []
    node = False

    value_re = re.compile('[vl]a[bl][eu][el]="([^"]+)')
    name_re = re.compile('name="([^"]+)')

    with open(xgmml, 'r') as g_file :
        with open(output, 'w') as w_file :
            for line in g_file:
                if '</node>' in line :   

                    x = ''

                    for header_name in header_order :
                        if '_IDs' in header_name:
                            x = header_name

                    if "IDs_rep_node" not in header_order and x == '' :
                        x = "Node_id"
                    elif x == '' :
                        x = "IDs_rep_node"

                    num_items = len(dict_columns[x])

                    dict_columns = {item:value if len(value) == num_items else ' -- '.join(value) for item, value in dict_columns.items()}
                    dict_columns = {item:value if '--' not in value else '' for item, value in dict_columns.items()}

                    if header :
                        w_file.write('{}\n'.format('\t'.join(header_order)))
                        header = False
                    else :
                        for index in range(num_items) :
                            line2write = ''

                            for column in header_order :
                                if column in dict_columns :
                                    if type(dict_columns[column]) == list :
                                        line2write += '{}\t'.format(dict_columns[column][index])
                                    else :
                                        line2write += '{}\t'.format(dict_columns[column])                      

                            w_file.write(f'{line2write.rstrip()}\n') 

                    dict_columns = {item:[] for item, value in dict_columns.items()}
                    node = False

                elif 'node id' in line :
                    node = True 
                    name = 'node id'
                    value = value_re.search(line).group(1)    

                    if name in translate_dict :
                        new_name = translate_dict[name]

                        if name not in dict_columns :
                            dict_columns[new_name] = [value]
                        else :
                            dict_columns[new_name].append(value)

                        if new_name not in header_order:
                            header_order.append(new_name)                                     

                elif 'list' not in line and '</att>' not in line and node:
                    name = name_re.search(line).group(1)
                    try :
                        value = value_re.search(line).group(1)
                    except AttributeError:
                        value = ''
                
                    if name in translate_dict :
                        new_name = translate_dict[name]

                        if name not in dict_columns :
                            dict_columns[new_name] = [value]
                        else :
                            dict_columns[new_name].append(value)

                        if new_name not in header_order:
                            header_order.append(new_name)
    return

##########################################################################################
##########################################################################################
##
##                                Main
##
##########################################################################################
##########################################################################################


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
     description=dedent("""Convert xgmml from SSN to table""") )

general_option = parser.add_argument_group(title = "General input dataset options")
general_option.add_argument("-g",'--xgmml',
                            metavar="<XGMML>",
                            dest="xgmml",
                            help="XGMML file from the analysis of EFI-EST : https://efi.igb.illinois.edu/efi-est/",
                            required=True)

general_option.add_argument("-o",'--output',
                            default=None,
                            dest="output",
                            metavar='<OUTPUT>',
                            help="Name of the output file (default: [NAME_OF_XGMML]_table.tsv)")

##########################################################################################

"""
Unused
------

general_option.add_argument("-f",'--full',
                            dest="full",
                            action='store_true',
                            help="Option that allows to have a table with all the columns that appear in the xgmml. Default columns are : ???")
general_option.add_argument("-t",'--taxonomy',
                            action='store_true',
                            dest="taxonomy",
                            help="Add the taxonomy if present in the file, to have the best result of this feature \
                                  please use the full network not a reduced/concatenated one. Else only unique field will be written")
"""



args = parser.parse_args()

##########################################################################################

if args.output :
    OUTPUT = args.output
else :
    OUTPUT = os.path.join(os.getcwd(), '{}_table.tsv'.format(os.path.basename(args.xgmml)))

##########################################################################################

XGMML = args.xgmml

##########################################################################################

xgmml2tsv_full(XGMML, OUTPUT)

'''
if args.full :
    xgmml2tsv_full(XGMML, OUTPUT)
elif args.taxonomy :
    xgmml2tsv_taxonomy(XGMML, OUTPUT)
else :
    xgmml2tsv_default(XGMML, OUTPUT)
'''