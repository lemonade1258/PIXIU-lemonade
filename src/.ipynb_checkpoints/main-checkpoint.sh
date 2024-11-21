MODEL_PATH="/root//root/autodl-tmp/models/finma-120"
TOKENIZER_PATH="${MODEL_PATH}"  # 如果 tokenizer 和 model 使用相同路径

# 执行命令
python eval.py --model "hf-causal-vllm" \
               --model_args "pretrained=${MODEL_PATH},tokenizer=${TOKENIZER_PATH},trust_remote_code=True" \
               --tasks "AuditQA_zh_Audit_document_generation","AuditQA_zh_Audit_item_risk_problem_analysis"
