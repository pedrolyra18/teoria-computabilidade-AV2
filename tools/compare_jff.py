import xml.etree.ElementTree as ET
import os, sys

ROOT = os.getcwd()
MT_JFF = os.path.join(ROOT, 'implementacoes', 'mt-multifita', 'palindromo.jff')
PDA_JFF = os.path.join(ROOT, 'implementacoes', 'pda', 'anbn.jff')

# parse MT jff

def parse_mt_jff(path):
    tree = ET.parse(path)
    root = tree.getroot()
    # states
    id_to_name = {}
    for state in root.findall('.//state'):
        sid = state.get('id')
        name = state.get('name')
        if sid and name:
            id_to_name[sid] = name
    transitions = {}
    for t in root.findall('.//transition'):
        fr = t.find('from').text.strip()
        to = t.find('to').text.strip()
        # collect reads per tape
        reads = {}
        writes = {}
        moves = {}
        for r in t.findall('read'):
            tape = r.get('tape')
            txt = r.text
            txt = '' if txt is None else txt
            reads[int(tape)] = txt
        for w in t.findall('write'):
            tape = w.get('tape')
            txt = w.text
            txt = '' if txt is None else txt
            writes[int(tape)] = txt
        for m in t.findall('move'):
            tape = m.get('tape')
            txt = m.text.strip() if m.text else ''
            moves[int(tape)] = txt
        # assume 2 tapes
        r1 = reads.get(1, '')
        r2 = reads.get(2, '')
        w1 = writes.get(1, '')
        w2 = writes.get(2, '')
        m1 = moves.get(1, '')
        m2 = moves.get(2, '')
        key = (id_to_name.get(fr, fr), r1 if r1!='' else 'B', r2 if r2!='' else 'B')
        transitions[key] = (id_to_name.get(to, to), w1 if w1!='' else 'B', m1, w2 if w2!='' else 'B', m2)
    return transitions


def parse_pda_jff(path):
    tree = ET.parse(path)
    root = tree.getroot()
    id_to_name = {}
    for state in root.findall('.//state'):
        sid = state.get('id')
        name = state.get('name')
        if sid and name:
            id_to_name[sid] = name
    transitions = {}
    for t in root.findall('.//transition'):
        fr = t.find('from').text.strip()
        to = t.find('to').text.strip()
        read = t.find('read')
        pop = t.find('pop')
        push = t.find('push')
        rtxt = '' if read is None or read.text is None else read.text
        poptxt = '' if pop is None or pop.text is None else pop.text
        pushtxt = '' if push is None or push.text is None else push.text
        key = (id_to_name.get(fr, fr), rtxt, poptxt)
        transitions[key] = (id_to_name.get(to, to), pushtxt)
    return transitions


if __name__ == '__main__':
    # import simulator deltas
    sys.path.append(os.path.join(ROOT, 'implementacoes', 'mt-multifita'))
    sys.path.append(os.path.join(ROOT, 'implementacoes', 'pda'))
    try:
        import simulador_mt
        import simulador_pda
    except Exception as e:
        print('ERROR importing simulators:', e)
        sys.exit(2)

    mt_sim = simulador_mt.construir_transicoes()
    pda_sim = simulador_pda.construir_transicoes()

    mt_jff = parse_mt_jff(MT_JFF)
    pda_jff = parse_pda_jff(PDA_JFF)

    print('MT: transitions in simulator:', len(mt_sim))
    print('MT: transitions in JFF    :', len(mt_jff))

    # compare keys
    sim_keys = set(mt_sim.keys())
    jff_keys = set(mt_jff.keys())
    missing_in_jff = sim_keys - jff_keys
    extra_in_jff = jff_keys - sim_keys
    print('\nMT missing in JFF (show up to 20):')
    for i,k in enumerate(sorted(missing_in_jff)):
        if i>=20: break
        print(' ',k,'->',mt_sim[k])
    print('\nMT extra in JFF (show up to 20):')
    for i,k in enumerate(sorted(extra_in_jff)):
        if i>=20: break
        print(' ',k,'->',mt_jff[k])

    print('\nPDA: transitions in simulator:', len(pda_sim))
    print('PDA: transitions in JFF    :', len(pda_jff))
    sim_keys = set(pda_sim.keys())
    jff_keys = set(pda_jff.keys())
    missing_in_jff = sim_keys - jff_keys
    extra_in_jff = jff_keys - sim_keys
    print('\nPDA missing in JFF (show up to 20):')
    for i,k in enumerate(sorted(missing_in_jff)):
        if i>=20: break
        print(' ',k,'->',pda_sim[k])
    print('\nPDA extra in JFF (show up to 20):')
    for i,k in enumerate(sorted(extra_in_jff)):
        if i>=20: break
        print(' ',k,'->',pda_jff[k])

    # If no differences, print OK
    if not (missing_in_jff or extra_in_jff):
        print('\nAll transitions match between simulators and JFFs.')
    else:
        print('\nDifferences found; consider patching JFF or simulator to align.')
