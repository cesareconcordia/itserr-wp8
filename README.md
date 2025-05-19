## ITSERR WP8: CRitical Edition ONTology Enhanced per la Bibbia in latino.

Questa repository contiene i file RDF con la rappresentazione della Bibbia in latino (edizione Vulgata Weber-Gryson ed edizione S_VL (Sabatier)) ed il codice Python per la creazione dei set di dati.

Il codice è composto da 4 notebook Python ed una libreria software, ed implementa le seguenti funzionalità:

* lemmatizzazione dei testi: per ciascun testo vengono individuati i lemmi associati alle forme
* creazione dei grafi RDF: implementazione degli assiomi definiti nell'ontologia

 
L'ontologia creata per definire la struttura dei dataset  è denominata CRitical Edition ONTology Enhanced, per brevità CREONTE ed è un’ontologia applicativa espressa nel linguaggio OWL 2 DL, costruita come segue:

* ontologia top di riferimento: CIDOC-CRM nella versione OWL 2 DL detta “Erlangen”;
* principali ontologie di dominio: LRMoo per la rappresentazione delle risorse bibliografiche (“a high-level conceptual reference model for bibliographic information managed by libraries of all kinds”), CEO per la rappresentazione dell’edizione critica e dell’apparato relativo, TRESONT per la rappresentazione del contenuto e della struttura di opere testuali.

L'ontologia è descritta in dettaglio in questo [documento](https://docs.google.com/document/d/1n-OlAy1KleovGgHV4ZHhOSgkgMfsOKPDWT603_fic5k/edit?tab=t.0#heading=h.ng7sdvi05k6u).

#### Autori: 
Carlo Meghini, Cesare Concordia

info: [cesare.concordia@isti.cnr.it](mailto:cesare.concordia@isti.cnr.it)