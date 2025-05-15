'''
Created on Dec 9, 2024

@author: cesare
'''
import ast
import sys
import numpy as np
import pandas as pd
import rdflib
import matplotlib.pyplot as plt
# importing useful Python utility libraries we'll need
from collections import Counter, defaultdict
import itertools
import arpeggio as peg
import json
import re
import yaml
import os
import errno
from bs4 import BeautifulSoup, element, NavigableString, Comment, XMLParsedAsHTMLWarning
import warnings
import requests
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON



class OsisParser:
    lilaurl=''
    lilasparqlep=''
    lilaheaders={'Content-type':'application/x-www-form-urlencoded;charset=utf-8'}
    punct=['.', ',', ':', ';', '?', '!', '†', '※', '(', ')', '-', '..', '"', '[', ']', '•']
    def __init__(self):
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        self._loadConfig(self)
        
    @staticmethod
    
    def _loadConfig(self):
        if (os.path.isfile('config.yaml')):
            configfile="config.yaml"
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "config.yaml")
        try:
            with open(configfile, 'r') as stream:
                try:
                    conf=yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError:
            print('Warning config.yaml file not present! Please create it and set the values, store it in the main directory')
        
        self.inputsource=conf['INPUT_SOURCE']
        self.lilaurl=conf['LILA_TEXTLINKER']
        self.lilasparqlep=conf['LILA_SPARQLEP']
    def read_tei(self, tei_file):
        with open(tei_file, 'r') as tei:
            soup = BeautifulSoup(tei, features='lxml') #'lxml')
            return soup
        raise RuntimeError('Cannot generate a soup from the input')

    def is_book(self, tag):
        return tag.has_attr('type') and tag.has_attr('osisid') and tag['type']=='book'

    class TEIFile_PreProcess(object):
        def __init__(self, filename, idres=0):
            self.filename = filename
            # self.soup = self.read_tei(filename)
            with open(filename, 'r') as tei:
                self.soup = BeautifulSoup(tei, "lxml")
            self._text = None
            self.idres=idres;
    
    
        @property 
        def getVerses (self):
            result=[]
            for chapter in self.soup.body.find_all("chapter"):
                if ('eid' in chapter.attrs):
                    continue
                
                chosisid=chapter.attrs['osisid']
               
                chtitle=chapter.next_sibling.next_sibling.get_text()
                vsid=''
                vosisid=''
                vtext=''
                for ci in chapter.next_sibling.next_sibling.next_sibling.next_sibling.children:
                    if (not isinstance(ci, NavigableString)):
            
                        if (ci.has_attr('sid')):
                            
                            vsid=ci['sid']
                            vosisid=ci['osisid']
                        if (isinstance(ci.next_sibling, NavigableString) and ci.next_sibling.string.strip()!=''):
    #                         print(ci.next_sibling)
                            vtext=ci.next_sibling
                        if (ci.has_attr('eid')):
    #                         print (ci['eid'])
    #                         result.append([chtitle, chsid, chosisid, vsid, vosisid, vtext])
                            result.append([vsid.split('.')[0], vosisid, vtext])
            return result
    
        @property 
        def getTitoloOpera (self):
            result=[]
            titoloOpera=''
            for header in self.soup.body.find_all('header'):
                titoloOpera=header.find('title').get_text()
            return titoloOpera
                
        @property 
        def getLangOpera (self):
            result=[]
            langOpera=''
            
            for ot in self.soup.body.find_all('osisText'):
                print (ot)
                if ot.has_attr('xml:lang'):
                    langOpera=ot['xml:lang']
                
            return langOpera
        @property 
        def getIdOpera (self):
            result=[]
            idOpera=''
            
            for header in self.soup.body.find_all('header'):
                idOpera=header.find('identifier').get_text()
                
            return idOpera
        
        
    def getDataFrame(self, source, files):
        df_all=pd.DataFrame()
        for fl in tqdm(files):
            tei = self.TEIFile_PreProcess(f'{self.inputsource}{source}/{fl.lower()}.xml', 0)
            rimepre=tei.getVerses
            data_pc_pre = pd.DataFrame(rimepre,columns=['libro','idverso', 'testo'])
            # parti=data_pc_pre.libro.unique()
            data_pc_pre['numverso']=data_pc_pre['idverso'].apply(lambda y: int(y.split('.')[2]))
            data_pc_pre['numcap']=data_pc_pre['idverso'].apply(lambda y: f"{y.split('.')[0]}.{y.split('.')[1]}")
            df_all=pd.concat([df_all, data_pc_pre], ignore_index=True)
        print('Creating IRIs...')
        df_all['irifrag']=df_all['testo'].apply(lambda y: df_all.index[df_all['testo']==y].tolist()[0])
        print ('done.')
        return df_all[['libro', 'idverso', 'numcap', 'numverso', 'testo', 'irifrag']]
    
    def resolveLemmiIn(self, verso, rif, idverso, ni):
        myd=[]
        for si in self.punct:
            verso=verso.replace(si, '')
        response=requests.post(self.lilaurl, headers=self.lilaheaders, json={"text":verso})
        res=json.loads(response.text)
#         print (f"{verso}")
        # if (not ni%50):
        #     print(ni)
        sentences =res['sentences']
        for sent in sentences:
            for ite in sent:
#             print (ite)
                ite["irifrag"]=rif
                myd.append(ite)
        return myd
    
    def getLemmi(self, df_forme):
        d_lemmi= []
        # tqdm.pandas(desc='My bar!')
        for ind, row in tqdm(df_forme.iterrows()):
            rset=self.resolveLemmiIn(row.testo, row.irifrag, row.idverso, ind)
            d_lemmi=d_lemmi+rset
        res=pd.DataFrame(d_lemmi)
        return res
    
    def getLemmaFromLiLa(self, forma):

        q="""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX lila: <http://lila-erc.eu/ontologies/lila/>
            PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>   
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        
            SELECT ?lemma  ?wr ?pos ?infl_ty (GROUP_CONCAT(distinct ?hg; separator=", ") as ?gen)  (GROUP_CONCAT(DISTINCT ?lvstr ;separator=", ") as ?l_variants) (GROUP_CONCAT(DISTINCT ?owr ;separator=", ") as ?o_wr)
            WHERE {
                  {
                  FILTER (?wr='"""+forma+"""') .
                  VALUES ?types {lila:Lemma lila:Hypolemma}
                  ?lemma rdf:type ?types;
                      lila:hasInflectionType ?ity;
                      lila:hasPOS ?pos.
                  ?ity rdfs:label ?infl_ty.
                  ?lemma rdfs:label ?wr .
                  ?lemma ontolex:writtenRep ?owr.
                      OPTIONAL { ?lemma lila:lemmaVariant ?lv .
                                  ?lv rdfs:label ?lvstr .}
                    OPTIONAL {
                      ?lemma lila:hasGender ?hg .
                    }
                  }
            } group by ?lemma ?pos ?wr ?infl_ty ?lemma_wr
        """
   
        ret='test'
        sparql = SPARQLWrapper(self.lilasparqlep)
        sparql.setReturnFormat(JSON)
      
        sparql.setQuery(q)
        try:
            ret = sparql.queryAndConvert()

        except Exception as e:
            print(e)
        res=[]
        
        for r in ret["results"]["bindings"]:
            resitem={}
            resitem['iri']=r['lemma']['value']
            resitem['lemma']=r['wr']['value']
            resitem['pos']=r['pos']['value'].replace('http://lila-erc.eu/ontologies/lila/', 'lila:')
            gend=r['gen']['value'].replace('http://lila-erc.eu/ontologies/lila/', 'lila:')
            resitem['gender']=gend
            resitem['varianti']=r['l_variants']['value']
            resitem['wrrep']=r['o_wr']['value']
            res.append(resitem)
        res_df=pd.DataFrame(res)
        return res_df