import pytest
import os
import time


@pytest.mark.parametrize('vocab_file', ['/tmp/vocab'])
def test_read_vocab(BPE, vocab_file):
    vocab = BPE(vocab_path=vocab_file).read_vocab_file()
    print("Vocab from file: {}".format(vocab))
    assert all(isinstance(k, str) for k in vocab.keys())
    assert all(isinstance(v, int) for v in vocab.values())


@pytest.mark.parametrize('codes_file', ['/tmp/codes'])
def test_read_codes(BPE, codes_file):
    codes, reverse_codes = BPE(codes_path=codes_file).read_bpe_file()
    print("Codes: {}".format(codes))
    print("Reverse codes: {}".format(reverse_codes))
    assert all(isinstance(k, tuple) for k in codes.keys())
    assert all(isinstance(v, int) for v in codes.values())
    assert all(isinstance(k, str) for k in reverse_codes.keys())
    assert all(isinstance(v, tuple) for v in reverse_codes.values())


@pytest.mark.parametrize('vocab_file', ['/tmp/vocab'])
def test_vocab(BPE, train_text, vocab, vocab_file):
    BPE.create_vocab_file(train_text, vocab_file)
    with open(vocab_file, 'r') as f:
        t_vocab = f.read()

    assert os.path.exists(vocab_file)
    assert t_vocab == vocab


@pytest.mark.parametrize('code_file,n_codes', [('/tmp/codes', 10)])
def test_learn_bpe(BPE, train_text, codes, code_file, n_codes):
    BPE.create_bpe_file(train_text, n_codes, code_file)
    with open(code_file, 'r') as f:
        t_codes = f.read()

    assert os.path.exists(code_file)
    assert t_codes == codes


@pytest.mark.parametrize('vocab_file,codes_file', [
    ('/tmp/vocab', '/tmp/codes')
])
def test_bpe_from_python(BPE, output, test_text, vocab_file, codes_file):
    res_f = BPE.apply_bpe_from_files(test_text, codes_file, vocab_file)

    bpe = BPE(vocab_path=vocab_file, codes_path=codes_file)
    bpe.load()

    res = bpe.apply_bpe(test_text)
    print("BPEs output: {}".format(res))
    print("BPE_f output: {}".format(res_f))
    # assert res == output
    assert res == res_f
    assert res_f == output


@pytest.mark.parametrize('vocab_file,codes_file', [
    ('/tmp/vocab', '/tmp/codes')
])
def test_file_vs_mem_time(BPE, output, test_text, vocab_file, codes_file):
    N = 1000
    # check from file time
    f_time = 0
    for _ in range(N):
        s = time.time()
        BPE.apply_bpe_from_files(test_text, codes_file, vocab_file)
        f_time += time.time() - s

    # check time from memory
    m_time = 0
    start = time.time()
    bpe = BPE(vocab_path=vocab_file, codes_path=codes_file)
    bpe.load()
    m_time += time.time() - start
    for _ in range(N):
        s = time.time()
        bpe.apply_bpe(test_text)
        m_time += time.time() - s

    print("Time from-file: {:.4f} | from-mem: {:.4f}".format(f_time, m_time))
    assert f_time > m_time

