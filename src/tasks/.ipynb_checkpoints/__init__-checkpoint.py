import sys

sys.path.append('../financial-evaluation')

from pprint import pprint
from typing import List, Union

import json
import lm_eval.base

from . import flare

TASK_REGISTRY = {
    "flare_es_financees": flare.ESFINANCEES,
    "flare_es_multifin": flare.ESMultiFin,
    "flare_es_efp": flare.ESEFP,
    "flare_es_efpa": flare.ESEFPA,
    "flare_es_fns": flare.ESFNS,
    "flare_es_tsa": flare.ESTSA,
    "flare_fpb": flare.FPB,
    "flare_fiqasa": flare.FIQASA,

    # "flare_ner": flare.ZHNER,
    "flare_finqa": flare.FinQA,
    "flare_convfinqa": flare.ConvFinQA,
    "flare_headlines": flare.Headlines,
    "flare_finer_ord": flare.FinerOrd,
    "flare_fomc": flare.FOMC,
    "flare_german": flare.German,
    "flare_australian": flare.Australian,
    "flare_fomc": flare.FOMC,
    "flare_ectsum": flare.ECTSUM,
    "flare_edtsum": flare.EDTSUM,
    "flare_finarg_ecc_auc": flare.FinargECCAUC,
    "flare_finarg_ecc_arc": flare.FinargECCARC,
    "flare_cd": flare.CD,
    "flare_multifin_en": flare.MultiFinEN,
    "flare_tsa": flare.TSA,
    "flare_cfa": flare.CFA,
    "flare_ma": flare.MA,
    "flare_causal20_sc": flare.Causal20SC,
    "flare_finarg_ecc_arc": flare.FINARGECCARC,
    "flare_finarg_ecc_auc": flare.FINARGECCAUC,
    "flare_mlesg": flare.MLESG,
    "flare_fnxl": flare.FNXL,
    "flare_fsrl": flare.FSRL,
    "flare_tatqa": flare.TATQA,
    "flare_finred": flare.FinRED,
    "flare_cra_lendingclub": flare.lendingclub,
    "flare_cra_ccf": flare.ccf,
    "flare_cra_ccfraud": flare.ccfraud,
    "flare_cra_polish": flare.polish,
    "flare_cra_taiwan": flare.taiwan,
    "flare_cra_portoseguro": flare.portoseguro,
    "flare_cra_travelinsurace": flare.travelinsurace,
    "flare_sm_bigdata": flare.StockMovementBigData,
    "flare_sm_acl": flare.StockMovementACL,
    "flare_sm_cikm": flare.StockMovementCIKM,
    "flare_en_finterm": flare.FINTERM,
    "flare_en_acronym": flare.ACRONYM,
    **flare.SM_TASKS,
    "flare_finarg_ecc_auc_test": flare.FINARGECCAUC_test,
    "flare_edtsum_test": flare.EDTSUM_test,

    "flare_finnl": flare.FinNL,

    "AuditQA_zh_audit_items_and_target": flare.AuditQA_zh_audit_items_and_target,
    "AuditQA_zh_audit_method_and_material": flare.AuditQA_zh_audit_method_and_material,
    "AuditQA_zh_audit_problem_describe": flare.AuditQA_zh_audit_problem_describe,
    "AuditQA_zh_audit_problem_summary": flare.AuditQA_zh_audit_problem_summary,
    "AuditQA_zh_Audit_legal_relevant_quesiton": flare.AuditQA_zh_Audit_legal_relevant_quesiton,
    "AuditQA_zh_Definition_of_audit_entity": flare.AuditQA_zh_Definition_of_audit_entity,
    "AuditQA_zh_Other_question": flare.AuditQA_zh_Other_question,
    "AuditQA_zh_recommend_appropriate_laws": flare.AuditQA_zh_recommend_appropriate_laws,

    "AuditRE_RE": flare.AuditRE_RE,

    "AuditNL_Audit_item_entity_classification": flare.AuditNL_Audit_item_entity_classification,
    "AuditNL_audit_problem_entity_classification": flare.AuditNL_audit_problem_entity_classification,
    "AuditNL_legal_name_classification": flare.AuditNL_legal_name_classification,

    "flare_ner": flare.NER,

    "AuditQA_zh_Audit_document_generation": flare.AuditQA_zh_Audit_document_generation,
    "AuditQA_zh_Audit_item_risk_problem_analysis": flare.AuditQA_zh_Audit_item_risk_problem_analysis,

    
    "test_for_long_question": flare.test_for_long_question,

    "AuditNL_Audit_item_entity_classification_optimization": flare.AuditNL_Audit_item_entity_classification_optimization,
    "audit_problem_entity_classification_optimization": flare.audit_problem_entity_classification_optimization,
    "legal_name_classification_optimization": flare.legal_name_classification_optimization,

    "ZHFinEval": flare.ZHFinEval,
    "ZHAstock": flare.ZHAstock,
    "ZHFinNA": flare.ZHFinNA

}

ALL_TASKS = sorted(list(TASK_REGISTRY))

_EXAMPLE_JSON_PATH = "split:key:/absolute/path/to/data.json"


def add_json_task(task_name):
    """Add a JSON perplexity task if the given task name matches the
    JSON task specification.

    See `json.JsonPerplexity`.
    """
    if not task_name.startswith("json"):
        return

    def create_json_task():
        splits = task_name.split("=", 1)
        if len(splits) != 2 or not splits[1]:
            raise ValueError(
                "json tasks need a path argument pointing to the local "
                "dataset, specified like this: json="
                + _EXAMPLE_JSON_PATH
                + ' (if there are no splits, use "train")'
            )

        json_path = splits[1]
        if json_path == _EXAMPLE_JSON_PATH:
            raise ValueError(
                "please do not copy the example path directly, but substitute "
                "it with a path to your local dataset"
            )
        return lambda: json.JsonPerplexity(json_path)

    TASK_REGISTRY[task_name] = create_json_task()


def get_task(task_name):
    try:
        add_json_task(task_name)
        return TASK_REGISTRY[task_name]
    except KeyError:
        print("Available tasks:")
        pprint(TASK_REGISTRY)
        raise KeyError(f"Missing task {task_name}")


def get_task_name_from_object(task_object):
    for name, class_ in TASK_REGISTRY.items():
        if class_ is task_object:
            return name

    # this gives a mechanism for non-registered tasks to have a custom name anyways when reporting
    return (
        task_object.EVAL_HARNESS_NAME
        if hasattr(task_object, "EVAL_HARNESS_NAME")
        else type(task_object).__name__
    )


def get_task_dict(task_name_list: List[Union[str, lm_eval.base.Task]]):
    task_name_dict = {
        task_name: get_task(task_name)()
        for task_name in task_name_list
        if isinstance(task_name, str)
    }
    task_name_from_object_dict = {
        get_task_name_from_object(task_object): task_object
        for task_object in task_name_list
        if not isinstance(task_object, str)
    }
    assert set(task_name_dict.keys()).isdisjoint(set(task_name_from_object_dict.keys()))
    return {**task_name_dict, **task_name_from_object_dict}