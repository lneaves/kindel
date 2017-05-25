import sys
import argh
import pandas as pd

from Bio import SeqIO

from kindel import kindel


def consensus(bam_path: 'path to SAM/BAM file',
              realign: 'attempt to reconstruct reference around soft-clip boundaries'=False,
              min_depth: 'substitute Ns at coverage depths beneath this value'=2,
              min_overlap: 'match length required to close soft-clipped gaps'=7,
              clip_decay_threshold: 'read depth fraction at which to cease clip extension'=0.1,
              trim_ends: 'trim ambiguous nucleotides (Ns) from sequence ends'=False,
              uppercase: 'close gaps using uppercase alphabet'=False):
    '''Infer consensus sequence(s) from alignment in SAM/BAM format'''
    result = kindel.bam_to_consensus(bam_path,
                                     realign,
                                     min_depth,
                                     min_overlap,
                                     clip_decay_threshold,
                                     trim_ends,
                                     uppercase)
    print(result.report, file=sys.stderr)
    SeqIO.write(result.consensuses, sys.stdout,'fasta')


def weights(bam_path: 'path to SAM/BAM file',
            relative: 'output relative nucleotide frequencies'=False,
            no_confidence: 'skip confidence calculation'=False):
    '''Returns table of per-site nucleotide frequencies and coverage'''
    weights_df = kindel.weights(bam_path, relative, no_confidence)
    weights_df.to_csv(sys.stdout, sep='\t', index=False)


def features(bam_path: 'path to SAM/BAM file'):
    '''Returns table of per-site nucleotide frequencies and coverage including indels'''
    weights_df = kindel.features(bam_path)
    weights_df.to_csv(sys.stdout, sep='\t', index=False)


def variants(bam_path: 'path to SAM/BAM file',
             abs_threshold: 'absolute frequency (0-∞) threshold above which to call variants'=1,
             rel_threshold: 'relative frequency (0.0-1.0) threshold above which to call variants'=0.01,
             only_variants: 'exclude invariant sites from output'=False,
             absolute: 'report absolute variant frequencies'=False):
    '''Output variants exceeding specified absolute and relative frequency thresholds'''
    variants_df = kindel.variants(bam_path, abs_threshold, rel_threshold, only_variants, absolute)
    variants_df.to_csv(sys.stdout, sep='\t', index=False, na_rep=0)


def plot_depth(*args):
    '''Plot depth table(s) generated by `samtools depth` for one or more alignments'''
    depths = kindel.parse_samtools_depth(*args)
    kindel.plotly_samtools_depth(depths)


def plot_variants(*args):
    '''Plot variant table(s) generated by `kindel variants`'''
    variants = kindel.parse_variants(*args)
    kindel.plotly_variants(variants)


def plot_clips(bam_path: 'path to SAM/BAM file'):
    '''Plot sitewise soft clipping frequency across reference and genome'''
    return kindel.plotly_clips(bam_path)


def main():
    parser = argh.ArghParser()
    parser.add_commands([consensus,
                         weights,
                         features,
                         variants,
                         plot_depth,
                         plot_variants,
                         plot_clips])
    parser.dispatch()


if __name__ == '__main__':
    main()
