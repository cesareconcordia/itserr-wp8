## Dataset lingua latina (WP8)

Questa repository contiene i file RDF con la rappresentazione della Bibbia in latino, edizione Vulgata Weber-Gryson ed edizione S_VL (Sabatier).
L'ontologia usata è denominata CRitical Edition ONTology Enhanced, per brevità CREONTE. CREONTE è un’ontologia applicativa espressa nel linguaggio OWL 2 DL , costruita come segue:

* ontologia top di riferimento: CIDOC-CRM nella versione OWL 2 DL detta “Erlangen”;
* principali ontologie di dominio: LRMoo per la rappresentazione delle risorse bibliografiche (“a high-level conceptual reference model for bibliographic information managed by libraries of all kinds”), CEO per la rappresentazione dell’edizione critica e dell’apparato relativo, TRESONT per la rappresentazione del contenuto e della struttura di opere testuali.

Per funzionare nel contesto presente, l’ontologia CEO è riveduta e corretta. La revisione principale riguarda il fatto che CEO ridefinisce le classi e le proprietà che usa dalle altre ontologie, anziché importare queste ultime; le ontologie coinvolte sono: CIDOC-CRM, LRMoo, HICO, CAO, OA, e PROV. Nella versione emendata, queste ontologie sono importate e gli assiomi relativi alle loro classi e proprietà sono rimossi da CEO, con l’eccezione dell’ontologia HICO, che non essendo aggiornata importa ontologie obsolete (quali per esempio FRBR); quindi le classi le proprietà usate da CEO sono da questa ridefinite.

Revisioni riguardanti l’ontologia CEO:

	CEO usa il namespace <http://purl.org/critical-edition-ontology#> e non <http://iflastandards.info/ns/lrm/lrmoo/>
	CEO usa un nome diverso dall’originale per le proprietà inverse del CRM e di LRMoo, omettendo la “i” dopo il numero. Ad esempio, l’inversa di R15_has_fragment è R15_is_fragment_of e non R15i_is_fragment_of
	CEO dichiara R4_embodies inversa sia di R4_is_embodied_in che di R5_is_component_of, quest’ultima dipendenza è stata rimossa
	CEO dichiara F3_Manifestatiion sottoclasse di F3_Expression, questo assioma è stata rimosso Riguardo all’ontologia CIDOC-CRM, si sono riscontrate analoghe anomalie, con la ridefinizione del dominio e del range di alcune proprietà
	CEO aggiunge un’asserzione di tipo rdfs:seeAlso alla ri-definizione di ogni classe e proprietà. L’asserzione punta al documento di specifica dell’LRMoo versione 0.9, ora superato
