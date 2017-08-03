import subprocess
import json
import collections
import sys
import math
import random
import pdb

def solve(*args):
    # Run clingo with the provided argument list and return the parsed JSON result.
    
    CLINGO = 'clingo-4.5.0-win64/clingo'
    
    clingo = subprocess.Popen(
        [CLINGO, '--outf=2'] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = clingo.communicate()
    if err:
        print(err)
    return parse_result(out)
    
def parse_result(out):
    # Take in the JSON output from clingo and 
    # return a dictionary of all of the predicates
    # expressed at the end of scratch.lp
    
    result = json.loads(out)
    
    assert len(result['Call']) > 0
    assert len(result['Call'][0]['Witnesses']) > 0
    
    witness = result['Call'][0]['Witnesses'][0]['Value']
    
    class identitydefaultdict(collections.defaultdict):
        def __missing__(self, key):
            return key
    
    preds = collections.defaultdict(set)
    env = identitydefaultdict()
    
    for atom in witness:
        if '(' in atom:
            left = atom.index('(')
            functor = atom[:left]
            arg_string = atom[left:]
            try:
                preds[functor].add( eval(arg_string, env) )
            except TypeError:
                pass # at least we tried...
            
        else:
            preds[atom] = True
    
    return dict(preds)
	
def render_level(design, width, height):
    #print(design['cell']) 
    val = {c:v for (v,c) in design['cell']}
    # row = {}
    # for c in val:
        # #print("{}".format(c))
        # if c[1] in row:
            # row[c[1]].append((c, val[c]))
            # row[c[1]] = sorted(row[c[1]], key=lambda tup: tup[0])
        # else:
			# row[c[1]] = [(c, val[c])]
    # #for i in range(0, len(row)):
    # #    print("{}: {}".format(i, row[i]))
    return val

if __name__ == '__main__':
    lvlWidth = 9
    lvlHeight = 9
    s = ""
    divisions = math.floor(math.sqrt(lvlWidth))
    
    for i in range(0, lvlWidth + 2):
        s += "- "
    
    # Get back design from clingo with our provided constants
    design = solve("sudoku.lp", "-c", "width=%d"%lvlWidth, "-c", "height=%d"%lvlHeight, "-c", "divs=%d"%divisions,'--sign-def=3','--seed='+str(random.randint(0,1<<30)))
    # Convert clingo output to usable output
    x = render_level(design, lvlWidth, lvlHeight)
    for h in range(0, lvlHeight):
        row = ""
        if h > 0 and h % divisions == 0:
            print(s)
        for w in range(0, lvlWidth):
            if w > 0 and w % divisions == 0:
                row += "| "
            row += str(x[(w, h)]) + " "
        print(row)
