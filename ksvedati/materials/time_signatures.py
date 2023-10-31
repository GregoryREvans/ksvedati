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
## total ##
##

all_signatures = evans.join_time_signature_lists(
    [
        reduced_signatures_01,
    ]
)
