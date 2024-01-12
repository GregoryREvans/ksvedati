import abjad
import evans

##
## 01 ##
##

signatures_01 = [abjad.TimeSignature((4, 4)) for _ in range(54)]

signatures_01.append(abjad.TimeSignature((1, 4)))  # for ending skip

fermata_measures_01 = [3, 6, 13, 27, 53]

reduced_signatures_01 = evans.reduce_fermata_measures(
    signatures_01, fermata_measures_01
)

##
## 02 ##
##

signatures_02 = [abjad.TimeSignature((4, 4)) for _ in range(44)]

signatures_02.append(abjad.TimeSignature((1, 4)))  # for ending skip

fermata_measures_02 = [2, 4, 10, 22, 43]
#25, 26, 27

reduced_signatures_02 = evans.reduce_fermata_measures(
    signatures_02, fermata_measures_02
)


##
## total ##
##

all_signatures = evans.join_time_signature_lists(
    [
        reduced_signatures_01,
    ]
)

all_duet_signatures = evans.join_time_signature_lists(
    [
        reduced_signatures_02,
    ]
)
