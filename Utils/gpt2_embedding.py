import numpy as np

def gpt2_embedding(txt):
    idx = tokenizer.encode(txt, max_length=1024, truncation=True)
    if len(idx) >= 1024:
        return None
    idx = np.array(idx)[None, :]

    emb = model(torch.tensor(idx))[0]
    hidden = np.array(emb[0])

    sent_emb = hidden.mean(0)
    return sent_emb