#!/bin/bash
WORKING_DIR=`pwd`

# Check sourmash version
VERSION=`sourmash -v | cut -d ' ' -f2`
echo -e "\n\nUsing Sourmash Version: $VERSION\n\n"

pip install scipy
pip install networkx
pip install matplotlib

# Specify kmer size for analysis
read -p "Enter kmer size (default=31): " KMER
read -p "Enter scaled size (default=1000): " SCALED
read -p "Compare genomes using Jaccard Index, Average Nucleotide Identity, or Containment? (JI/ANI/C): " COMPARE_OUTPUT
read -p "Generate sourmash plots? (Y/N): " PLOTS

# Prepping file to read genome IDs from
touch "fna_files_to_smash.txt"
for i in "$@"
do
    echo $i >> fna_files_to_smash.txt
done

# Sourmash Sketch
SKETCH_OUTDIR="sig_files_$KMER"
mkdir $SKETCH_OUTDIR

sourmash sketch dna -p k=$KMER,scaled=$SCALED --outdir $SKETCH_OUTDIR `cat fna_files_to_smash.txt`

rm fna_files_to_smash.txt

# Sourmash Compare
cd $SKETCH_OUTDIR

COMPARE_FILE=compare_$KMER

if [[ $COMPARE_OUTPUT == "JI" ]]
then
    sourmash compare --ksize $KMER --output $COMPARE_FILE.JI.binary --csv $COMPARE_FILE.JI.csv *
elif [[ $COMPARE_OUTPUT == "ANI" ]]
then
    sourmash compare --ksize $KMER --ani --output $COMPARE_FILE.ANI.binary --csv $COMPARE_FILE.ANI.csv *
elif [[ $COMPARE_OUTPUT == "C" ]]
then
    sourmash compare --ksize $KMER --containment --output $COMPARE_FILE.C.binary *
fi

# Sourmash Plot
if [[ $PLOTS == "Y" ]]
then
    echo -e "\n\nGenerating plots..."
    sourmash plot --pdf $COMPARE_FILE.*.binary
elif [[ $PLOTS == "N" ]]
then
    echo -e "\n\nIgnoring plot generation..."
else
    echo -e "\n\nIncorrect answer format. Generating plots..."
    sourmash plot --pdf $COMPARE_FILE.*.binary
fi

# copy and edit python script for later
#read -p "Large dataset? Will need to shrink node/edge size (Y/N): " SIZE
read -p "Keep node labels? (Not reccomended for large datasets) (Y/N): " LABELS
read -p "Remove self-loops? (Hard to visualise in large datasets, but may need downstream) (Y/N): " LOOPS
read -p "Remove edges of values less than? (0-1): " EDGES

CSV_MATRIX=$COMPARE_FILE.$COMPARE_OUTPUT.csv
FILE_BASE=$COMPARE_FILE.$COMPARE_OUTPUT

cat $WORKING_DIR/smash_process.py | sed "s/WEIRDNAME_1/$CSV_MATRIX/g" | sed "s/WEIRDNAME_2/processed_$CSV_MATRIX/g" | sed "s/WEIRDNAME_3/$FILE_BASE/g" > smash_process_1.py

# change script to remove or keep node labels
if [[ $LABELS == "Y" ]]
then
    echo "Will keep labels in network graphs..."
    cat smash_process_1.py > smash_process_2.py
elif [[ $LABELS == "N" ]]
then
    cat smash_process_1.py | sed "s/with_labels=True/with_labels=False/g" > smash_process_2.py
else
    echo "Incorrect answer format, will remove node labels..."
    cat smash_process_1.py | sed "s/with_labels=True/with_labels=False/g" > smash_process_2.py
fi

# change script to remove or keep self loops
if [[ $LOOPS == "Y" ]]
then
    echo "Will remove self-loops..."
    cat smash_process_2.py | sed "s/#BEEP//g" | sed "s/LOOPED/G2/g" > smash_process_3.py
elif [[ $LOOPS == "N" ]]
then
    echo "Will keep self-loops..."
    cat smash_process_2.py | sed "s/LOOPED/G1/g" > smash_process_3.py
else
    echo "Incorrect answer format, removing self-loops..."
    cat smash_process_2.py | sed "s/#BEEP//g" | sed "s/LOOPED/G2/g" > smash_process_3.py
fi

# change script to remove edges of certain value
cat smash_process_3.py | sed "s/OMGEDGES/$EDGES/g" > smash_process_4.py

# change script to shrink node/edge size
#if [[ $SIZE == "Y" ]]
#then
#    echo "Shrinking node/edge size..."
#    cat smash_process_4.py | sed "s/BOOP/, node_size = 2, width = 0.005/g" > smash_process_5.py
#elif [[ $SIZE == "N" ]]
#then
#    echo "Ignoring node/edge size..."
#    cat smash_process_4.py | sed "s/BOOP//g" > smash_process_5.py
#else
#    echo "Incorrect answer format, ignoring node/edge size..."
#    cat smash_process_4.py | sed "s/BOOP//g" > smash_process_5.py
#fi

# change name of final python script and remove temp files
mv smash_process_4.py smash_process.py
rm smash_process_1.py; rm smash_process_2.py; rm smash_process_3.py; #rm smash_process_4.py

# Data Wrangling
mkdir processed_smash
python3 smash_process.py
mv processed_$CSV_MATRIX processed_smash/
mv network_$COMPARE_FILE.$COMPARE_OUTPUT.pdf processed_smash/
mv top5cliques_$FILE_BASE.csv processed_smash/



