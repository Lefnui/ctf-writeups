xorz
============

In this challenge, the flag is used as key in a repeating key xor. To make it more "secure", authors added a xor with a salt to produce the final output.
This does not add security as we know the salt, we start by xoring the output with it to get `plain ^ key`.

Now it is just a matter of recovering the key. To do it clean we should first try to figure out the size of the key. I had some code to do it, which did not give the correct result, so I bruteforced it instead.

For each keysize K, we divide the plaintext in K blocks. For example with K=3:

| block 1   | block 2  | block 3   |
| --------- |--------- | --------- |
| c1        | c2       | c3        |
| c4        | c5       | c6        |
| c7        | c8       | c9        |

For each block, we do a frequential analysis to determine the most likely key. Full instructions are available [here](https://cryptopals.com/sets/1/challenges/6).

As the text is quite long, it works well. We find that the keysize is 30, the plaintext is 
```
In faith I do not love thee with mine eyes,For they in thee a thousand errors note;But `tis my heart that loves what they despise,Who in despite of view is pleased to dote.Nor are mine ears with thy tongue`s tune delighted;Nor tender feeling to base touches prone,Nor taste, nor smell, desire to be invitedTo any sensual feast with thee alone.But my five wits, nor my five senses canDissuade one foolish heart from serving thee,Who leaves unswayed the likeness of a man,Thy proud heart`s slave and vassal wretch to be.Only my plague thus far I count my gain,That she that makes me sin awards me pain.
```
and the flag is:
`de1ctf{W3lc0m3tOjo1nu55un1ojOt3m0cl3W}`
