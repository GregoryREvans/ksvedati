import pathlib

import evans

import ksvedati

breaks = evans.Breaks(
    evans.Page(
        evans.System(measures=5, lbsd=(20, "(19 20 20 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(19 20 20 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(20, "(19 20 20 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(19 20 20 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(20, "(19 20 20 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(19 20 20 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(20, "(19 20 20 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(19 20 20 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(20, "(19 20 20 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(19 20 20 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=4, lbsd=(20, "(19 20 20 20)"), x_offset=1),
    ),
    time_signatures=ksvedati.reduced_signatures_01,
    default_spacing=(1, 38),  # 42
    spacing=[
        # (2, (1, 15)),
    ],
    bar_number=1,
)

output_path = pathlib.Path(__file__).parent

breaks.make_document_layout(path=output_path)
