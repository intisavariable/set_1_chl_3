import binascii
from scipy.stats import chisquare
from dataclasses import dataclass
from typing import Any

english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,  
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,  
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074  
]

@dataclass
class Result:
    xor_key: int
    decoded_text: str
    chi2score: list

def f_obs(inpt):
    count = []
    ignored = 0
    for i in range(26):
        count.append(0)

    for char in inpt:
        c = ord(char)
        if c >= 65 and c <= 90:# uppercase A-Z 
            count[c - 65] += 1
        elif c >= 97 and c <= 122:
            count[c-97] += 1  # lowercase a-z
        elif c >= 32 and c<=126:
            ignored += 1  # numbers and punct.
        elif c == 9 or c == 10 or c == 13:
            ignored += 1   # TAB, CR, LF  
        else:
            continue
    
    #print(count)
    return count

def main():
    encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'


    nums = binascii.unhexlify(encoded)
    result_objects = []
    for xor_key in range(256):
        decoded = ''.join(chr(b ^ xor_key) for b in nums)
        freq_obs = f_obs(decoded)
        if sum(freq_obs) == 0:
            continue
        else:
            for i in range(len(freq_obs)):
                freq_obs[i] = freq_obs[i] / len(decoded)
            result_objects.append(Result(xor_key, decoded, chisquare(f_obs= freq_obs, f_exp=english_freq)))
        
    result_objects.sort(key=lambda result: result.chi2score[0],reverse=True)

    for val in result_objects:
        output = '{} :: {} :: {}'.format(val.xor_key,val.decoded_text, val.chi2score[0])
        if output.isprintable() and val.chi2score[1] >= 0.05:        
            print(output)
            print("\n")


if __name__ == "__main__":
    main()