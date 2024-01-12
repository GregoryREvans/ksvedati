import pathlib

import evans

import ksvedati

breaks = evans.Breaks(
    evans.Page(
        evans.System(measures=6, lbsd=(50, "(14 24)"), x_offset=1),
        evans.System(measures=5, lbsd=(90, "(14 24)"), x_offset=1),
        evans.System(measures=5, lbsd=(140, "(14 24)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(14 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(60, "(14 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(120, "(14 20)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(14 20)"), x_offset=1),
        evans.System(measures=5, lbsd=(60, "(14 20)"), x_offset=1),
        evans.System(measures=3, lbsd=(120, "(14 20)"), x_offset=1),
    ),
    time_signatures=ksvedati.reduced_signatures_02,
    default_spacing=(1, 23),
    spacing=[
        # (193, (1, 30)),
        # (194, (7, 144)),  #
        # (195, (1, 30)),
        # (196, (1, 30)),
        # (197, (1, 30)),
        # (198, (7, 144)),  #
        # (199, (1, 30)),
        # (200, (1, 30)),
        # (201, (1, 30)),
        # (202, (1, 30)),
    ],
    bar_number=1,
)

output_path = pathlib.Path(__file__).parent

breaks.make_document_layout(path=output_path)
