import pathlib

import evans

import ksvedati

breaks = evans.Breaks(
    evans.Page(
        evans.System(measures=5, lbsd=(60, "(14 25 25 25)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(18 33 33 33)"), x_offset=1),
        evans.System(measures=5, lbsd=(80, "(18 33 33 33)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(18 33 33 33)"), x_offset=1),
        evans.System(measures=5, lbsd=(80, "(18 33 33 33)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(18 33 33 33)"), x_offset=1),
        evans.System(measures=5, lbsd=(80, "(18 33 33 33)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(18 33 33 33)"), x_offset=1),
        evans.System(measures=5, lbsd=(80, "(18 33 33 33)"), x_offset=1),
    ),
    evans.Page(
        evans.System(measures=5, lbsd=(1, "(18 33 33 33)"), x_offset=1),
        evans.System(measures=4, lbsd=(80, "(18 33 33 33)"), x_offset=1),
    ),
    time_signatures=ksvedati.all_signatures,
    default_spacing=(1, 25),
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
