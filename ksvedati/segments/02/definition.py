import pathlib

import abjad
import baca
import evans
import numpy as np

import ksvedati


def bowings(selections):
    leaves = abjad.select.leaves(selections)
    bowing = evans.CyclicList([r"\baca-full-downbow-markup", r"\baca-full-upbow-markup"], forget=False)
    for leaf in leaves:
        abjad.attach(abjad.Markup(bowing(r=1)[0]), leaf, direction=abjad.UP)


def swells(selections):
    leaves = abjad.select.leaves(selections)
    cyc_dynamics = evans.CyclicList(["p", "mp", "p", "f", "mf", "pp", "ff", "f", "p", "mp", "pp"], forget=False)
    cyc_hairpins = evans.CyclicList(["<", ">", "<", ">", ">", "<", ">", ">", "<", ">", "<"], forget=False)
    for leaf in leaves:
        dynamic = abjad.Dynamic(cyc_dynamics(r=1)[0])
        abjad.attach(dynamic, leaf)
    for leaf in leaves[:-1]:
        hairpin = abjad.StartHairpin(cyc_hairpins(r=1)[0])
        abjad.attach(hairpin, leaf)



maker = evans.SegmentMaker(
    instruments=ksvedati.duet_instruments,
    names=[
        '"Violin"',
        '"Violoncello"',
    ],
    abbreviations=[
        '"vn."',
        '"vc."',
    ],
    name_staves=True,
    fermata_measures=ksvedati.fermata_measures_02,
    commands=[
        evans.attach(
            "violin voice",
            abjad.Clef("treble"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "cello voice",
            abjad.Clef("bass"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.call(
            "Global Context",
            lambda _: evans.wrap_in_repeats(_, number_of_repeats=5),
            evans.select_measures([25, 26, 27], leaves=[0, 1, 2]),
        ),
        evans.attach(
            "violin voice",
            abjad.LilyPondLiteral(r"\staff-line-count #1"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "cello voice",
            abjad.LilyPondLiteral(r"\staff-line-count #1"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.MusicCommand(
            [
                ("violin voice", [0, 1]),
            ],
            evans.talea(
                [5, -3],
                4,
            ),
            evans.PitchHandler([0], staff_positions=True, clef="treble"),
            abjad.LilyPondLiteral(r'\boxed-markup "non-guiro clt." 1', site="after"),
            # evans.force_accidentals,
            evans.Callable(
                lambda _: baca.hairpin(_, "mf >o niente"),
                selector=lambda _: abjad.select.leaves(_),
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                # pieces=lambda _: abjad.select.leaves(_),
            ),
        ),
        evans.MusicCommand(
            [
                ("cello voice", 1),
            ],
            evans.note(),
            evans.PitchHandler([0], staff_positions=True, clef="bass"),
            abjad.LilyPondLiteral(r'\boxed-markup "on mute clt." 1', site="after"),
            evans.Callable(
                lambda _: baca.hairpin(_, "mf -- niente"),
                selector=lambda _: abjad.select.leaves(_) + [abjad.get.leaf(abjad.select.leaves(_)[-1], 1)],
            ),
        ),
        evans.MusicCommand(
            [
                ("violin voice", 3),
            ],
            evans.talea([3, 3, 2, 8], 16, rewrite=-1),
            evans.PitchHandler([["a", "g'"]]),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.LilyPondLiteral(r'\boxed-markup "guiro clt." 1', site="after"),
            evans.Callable(
                lambda _: baca.hairpin(_, "pp -- niente"),
                selector=lambda _: abjad.select.leaves(_) + [abjad.get.leaf(abjad.select.leaves(_)[-1], 1)],
            ),
        ),
        evans.MusicCommand(
            [
                ("violin voice", (5, 10)),
            ],
            evans.talea([3, 3, 2, 8], 16, rewrite=-1),
            evans.PitchHandler([["a", "g'"]]),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.LilyPondLiteral(r'\boxed-markup "guiro crine" 1', site="after"),
            evans.Callable(
                lambda _: baca.hairpin(_, "p -- niente"),
                selector=lambda _: abjad.select.leaves(_) + [abjad.get.leaf(abjad.select.leaves(_)[-1], 1)],
            ),
        ),
        evans.MusicCommand(
            [
                ("cello voice", (6, 10)),
            ],
            evans.talea(
                [_ * 4 for _ in [3, 1, 2, 4, 3, 2, 2]],
                8,
                extra_counts=[1, 0, -1, 1, 0, 2],
                preprocessor=evans.make_preprocessor(sum=True, eighths=True, fuse_counts=[3, 2, 2, 4, 2]),
                rewrite=-1,
            ),
            lambda _: abjad.tie(_),
            evans.PitchHandler([0], staff_positions=True, clef="bass"),
            abjad.LilyPondLiteral(r"\staff-line-count #1"),
            abjad.LilyPondLiteral(r'\boxed-markup "on mute crine" 1', site="after"),
            lambda _: swells(_),
        ),
        evans.call(
            "Global Context",
            evans.TempoSpannerHandler(
                tempo_list=[(2, 0, 1, "30"), (2, 0, 1, "60")],
                boolean_vector=[1],
                padding=4,
                staff_padding=2,
           ),
           selector=evans.select_measures([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
        ),
        evans.MusicCommand(
            [
                ("violin voice", (11, 22)),
            ],
            evans.talea([1], 2),
            evans.PitchHandler([["a", "g'"]]),
            evans.Callable(
                lambda _: baca.hairpin(_, "ppp < fff"),
                selector=lambda _: abjad.select.leaves(_, pitched=True),
            ),
            lambda _: baca.text_spanner(
                _,
                r"non-guiro(clt.) => crine(scratch)",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                # pieces=lambda _: [_ + [abjad.get.leaf(_[-1], 1)] for _ in abjad.select.runs(_)],
            ),
        ),
        evans.MusicCommand(
            [
                ("cello voice", (12, 22)),
            ],
            evans.talea([1, 2, 1, 3, 1], 4),
            evans.PitchHandler([["d", "bf"]]),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            lambda _: baca.text_spanner(
                _,
                [
                    r"\trem-one-markup",
                    "->",
                    r"\trem-two-markup",
                    "->",
                    r"\trem-one-markup",
                    "->",
                    r"\trem-three-markup",
                    "->",
                    r"\trem-two-markup",
                    "->",
                    r"\trem-five-markup",
                    "->",
                    r"\trem-four-markup",
                    "->",
                ],
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_),
            ),
            lambda _: abjad.tie(_),
            abjad.Markup(r"\markup { sempre \dynamic mp }")
        ),
        evans.MusicCommand(
            [
                ("violin voice", [23, 24]),
            ],
            evans.talea([1, 1, 1, 1, 1, 3], 4),
            evans.PitchHandler([["a", "g'"], ["a", "a'"], ["b", "a'"], ["b", "c''"], ["e'", "c''"], ["d'", "d''"]]),
            lambda _: abjad.glissando(_),
            # abjad.LilyPondLiteral(r"\staff-line-count #1"),
            # abjad.Markup(r"\markup {crine}"),
            lambda _: baca.text_spanner(
                _,
                r"scratch -|",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: [_ + [abjad.get.leaf(_[-1], 1)] for _ in abjad.select.runs(_)],
            ),
            abjad.Dynamic("f"),
        ),
        evans.MusicCommand(
            [
                ("cello voice", [23, 24]),
            ],
            evans.talea([1, 2, 2, 1, 2], 4),
            evans.PitchHandler([["d", "a"], ["b,", "a"], ["b,", "g"], ["f,", "g"], ["f,", "d"]]),
            lambda _: abjad.glissando(_),
            # abjad.LilyPondLiteral(r"\staff-line-count #1"),
            # abjad.Markup(r"\markup {crine}"),
            abjad.Dynamic("mf"),
        ),
        evans.MusicCommand(
            [
                ("violin voice", [25, 26, 27]),
            ],
            evans.talea([-4, 2, -2, 3, -2, 3, -2, 2, 2, -2], 8, rewrite=-1),
            evans.PitchHandler(["f'"]),
            lambda _: abjad.glissando(_),
            # abjad.LilyPondLiteral(r"\staff-line-count #1"),
            abjad.LilyPondLiteral(r'\boxed-markup "non-guiro (crine)" 1', site="after"),
            lambda _: baca.text_spanner(
                _,
                r"\spike-middle-markup -> \spike-top-markup -> \spike-middle-markup -> \spike-top-markup -> \spike-bottom-markup ->",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: [_ + [abjad.get.leaf(_[-1], 1)] for _ in abjad.select.runs(_)],
            ),
            lambda _: [abjad.tie(x) for x in abjad.select.runs(_) if 1 < len(x)],
        ),
        evans.MusicCommand(
            [
                ("cello voice", [25, 26, 27]),
            ],
            evans.talea([3, 3, 4, 2], 4),
            evans.PitchHandler([[-8, 2], [-8 + 4, 2 + 4], [-8 - 6, 2 - 6], [-8, 2], [-8 - 1, 2 - 1]]),
            evans.zero_padding_glissando,
            abjad.Clef("tenor"),
            # abjad.LilyPondLiteral(r"\staff-line-count #1"),
            # abjad.Markup(r"\markup {crine}"),
            lambda _: bowings(_),
            lambda _: abjad.attach(abjad.Glissando(), abjad.select.leaf(_, -1)),
            lambda _: abjad.attach(evans.make_fancy_gliss(3, 2, 3, 1, 3, 1, 0.5, right_padding=0.5, match=True), abjad.select.leaf(_, -1)),
            lambda _: abjad.attach(abjad.AfterGraceContainer([abjad.Chord("<e d'>16")]), abjad.select.leaf(_, -1)),
        ),
        evans.MusicCommand(
            [
                ("cello voice", (28, 34)),
            ],
            evans.note(),
            evans.PitchHandler([0], staff_positions=True, clef="tenor"),
            abjad.Dynamic("mp"),
            abjad.LilyPondLiteral(r"\staff-line-count #1"),
            abjad.LilyPondLiteral(r'\boxed-markup "on mute (legno)" 1', site="after"),
            evans.Attachment(
                abjad.AfterGraceContainer("a16 a16 a16"),
                selector=lambda _: abjad.select.leaf(_, 1, grace=False),
            ),
            evans.Attachment(
                abjad.LilyPondLiteral(r'\boxed-markup "battuto" 1', site="after"),
                selector=lambda _: abjad.select.leaf(_, 0, grace=True),
            ),
            evans.Attachment(
                abjad.AfterGraceContainer("a16 a16 a16"),
                selector=lambda _: abjad.select.leaf(_, 3, grace=False),
            ),
            evans.Attachment(
                abjad.AfterGraceContainer("a16 a16 a16 a16"),
                selector=lambda _: abjad.select.leaf(_, 4, grace=False),
            ),
        ),
        evans.MusicCommand(
            [
                ("violin voice", (29, 34)),
            ],
            evans.talea([1, 2, 1, -4, 3, 1, 2, 2, 3, 1], 4),
            evans.PitchHandler([0], staff_positions=True, clef="treble"),
            abjad.LilyPondLiteral(r"\staff-line-count #1"),
            abjad.Dynamic("mf"),
            lambda _: [baca.text_spanner(
                y,
                r"\spike-middle-markup -> \spike-top-markup -> \spike-middle-markup -> \spike-top-markup -> \spike-bottom-markup ->",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: [[x] for x in abjad.select.notes(_)],
            ) for y in abjad.select.runs(_)],
        ),
        evans.MusicCommand(
            [
                ("violin voice", (34, 40)),
            ],
            evans.talea([1, 2, 1, 4, 3, 1, 2, 2, 3, 1], 2),
            evans.zero_padding_glissando,
            evans.PitchHandler([[_, _ + 6] for _ in [-5, 0, -5, -1, -4, 2, 0, 5, -2]], staff_positions=True, clef="treble"),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.LilyPondLiteral(r'\boxed-markup "clt." 1', site="after"),
            abjad.Dynamic("p"),
        ),
        evans.MusicCommand(
            [
                ("cello voice", (34, 40)),
            ],
            evans.talea(
                [_ * 4 for _ in [1, 1, 2, 1, 4, 3, 1, 2, 2, 3]],
                8,
                extra_counts=[0, -1, 1, 0, 2, 1],
                preprocessor=evans.make_preprocessor(sum=True, eighths=True, fuse_counts=[2, 3, 2, 2, 4]),
                rewrite=-1,
            ),
            evans.zero_padding_glissando,
            evans.PitchHandler([[_, _ + 6] for _ in [-5, -4, -3, 5, -1, 4, -2, 3, -1, 2, 0, -1, -2]], staff_positions=True, clef="bass"),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.Clef("bass"),
            abjad.LilyPondLiteral(r'\boxed-markup "clt." 1', site="after"),
            abjad.Dynamic("p"),
        ),
        evans.MusicCommand(
            [
                ("violin voice", [40, 41, 42]),
            ],
            evans.note(),
            evans.PitchHandler(["g", "g", "f'"]),
            lambda _: abjad.glissando(_),
            evans.ArticulationHandler(["tremolo"]),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.LilyPondLiteral(r'\boxed-markup "crine" 1', site="after"),
            abjad.Dynamic("mp"),
            abjad.Tie(),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(_, 1),
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
        ),
        evans.MusicCommand(
            [
                ("cello voice", [40, 41, 42]),
            ],
            evans.note(),
            evans.PitchHandler(["c,", "c,", "f,"]),
            lambda _: abjad.glissando(_),
            evans.ArticulationHandler(["tremolo"]),
            abjad.LilyPondLiteral(r"\staff-line-count #5"),
            abjad.LilyPondLiteral(r'\boxed-markup "crine" 1', site="after"),
            abjad.Dynamic("mf"),
            abjad.Tie(),
            evans.Attachment(
                abjad.StartHairpin(">o"),
                selector=lambda _: abjad.select.leaf(_, 1),
            ),
            evans.Attachment(
                abjad.StopHairpin(),
                selector=lambda _: abjad.get.leaf(abjad.select.leaf(_, -1), 1),
            ),
        ),
        evans.call(
            "score",
            evans.SegmentMaker.beam_score_without_splitting,
            lambda _: abjad.select.components(_, abjad.Score),
        ),
        evans.attach(
            "Global Context",
            ksvedati.mark_30,
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "Global Context",
            ksvedati.met_30,
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([2], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([4], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([10], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([22], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([28], leaf=0),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uverylongfermata"',
            ),
            evans.select_measures([43], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(r'\bar "|."', site="after"),
            evans.select_measures([43], leaf=1),
        ),
        evans.attach(
            "cello voice",
            abjad.Markup(r"\colophon"),
            lambda _: abjad.select.leaf(_, -3),
            direction=abjad.DOWN,
        ),
    ],
    score_template=ksvedati.duet,
    transpose_from_sounding_pitch=True,
    time_signatures=ksvedati.signatures_02,
    clef_handlers=None,
    tuplet_bracket_noteheads=False,
    add_final_grand_pause=False,
    score_includes=[
        "abjad.ily",
        "../../build/segment_stylesheet.ily",
    ],
    segment_name="02",
    current_directory=pathlib.Path(__file__).parent,
    cutaway=False,
    beam_pattern="meter",
    beam_rests=True,
    barline="|.",
    rehearsal_mark="",
    fermata="scripts.ufermata",
    with_layout=True,
    mm_rests=False,
    extra_rewrite=False,  # should default to false but defaults to true
    print_clock_time=True,
)

maker.build_segment()
