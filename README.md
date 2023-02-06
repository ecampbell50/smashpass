# smashpass
Fast-pass to get network-graph/clique results from a SourMASH analysis
https://github.com/sourmash-bio/sourmash


smashpass:
- several prompts will appear asking to customise your sourmash/network plots
- answer with the correct format or default options will be used
- after completing sourmash it will then ask you prompts to customise your network graphs


# Using smashpass:
- working directory should containing .fna genome files, the smashpass.sh script and the smash_process.py script

```bash smashpass.sh *.fna``` 
- will ask for kmer-size, scaled size, method of comparing genomes (Jaccard index/ANI/Containment), and if you'd like to generate the sourmash plots
- customising network graphs includes: node labels, self-loops, removing edges less than a certain value
- scripts create temporary files
- may need to run on HPC if using large numbers of genomes

# Customisation
General points I've found while analysing 2121 S. suis genomes:
- local computer can easily create the .sig files, however cannot run comparisons. Will need HPC
- for advice on choosing the right kmer/scaled size and method of comparison, refer to sourmash readthedocs.io (very helpful, extensive)
https://sourmash.readthedocs.io/en/latest/
- when customising the network graphs, self-loops and node labels will likely cluter your graph and make it uninterpretable. Reccomended to remove these
- removing certain edge values is essential as every node will have some similarity to every other node, clique-formation not possible unless you specify
- if you have ran your sourmash separately and would just like to make a network graph, use the network_script.py file

# Network Script
This script requires the sourmash .csv output file. The sourmash standard .csv output is not compatible with my networkx code, so this script will convert it to a usable form. If you have done that yourself, you should be able to comment out the corresponding code and replace file names

Essential changes to make to the script:
- Line 9: must specify the file name of the sourmash output .csv
- Line 48: #ADD_EDGE_VALUE_HERE must be replaced with the pairwise similarity value of edges you'd like to remove (e.g, '0.6' will remove edges less than 0.6)
