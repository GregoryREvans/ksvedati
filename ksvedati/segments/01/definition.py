import pathlib

import abjad
import baca
import evans
import numpy as np

import ksvedati



def attach_material(selections):
    ties = abjad.select.logical_ties(selections)
    first_leaf = abjad.select.leaf(ties, 0)
    center_leaf = abjad.select.leaf(ties[len(ties) // 2], 0)
    last_leaf = abjad.select.leaf(ties, -1)
    cyc_dynamics = evans.CyclicList(["p", "f"], forget=False)
    cyc_hairpins = evans.CyclicList(["<", ">"], forget=False)
    for tie in ties:
        dynamic = abjad.Dynamic(cyc_dynamics(r=1)[0])
        abjad.attach(dynamic, tie[0])
    for tie in ties[:-1]:
        hairpin = abjad.StartHairpin(cyc_hairpins(r=1)[0])
        abjad.attach(hairpin, tie[0])
    start = abjad.bundle(abjad.StartTextSpan(
            left_text=abjad.Markup(r"\upright norm."),
            style="dashed-line-with-arrow",
        ),
        abjad.Tweak(r"\tweak staff-padding 6.5"),
    )
    middle = abjad.bundle(abjad.StartTextSpan(
            left_text=abjad.Markup(r"\upright msp."),
            right_text=abjad.Markup(r"\markup \upright st."),
            style="dashed-line-with-arrow",
        ),
        abjad.Tweak(r"\tweak staff-padding 6.5"),
    )
    middle_stop = abjad.StopTextSpan()
    final_stop = abjad.StopTextSpan()
    # abjad.tweak(start).staff_padding = 2
    # abjad.tweak(middle).staff_padding = 2
    abjad.attach(start, first_leaf)
    abjad.attach(middle_stop, center_leaf)
    abjad.attach(middle, center_leaf)
    abjad.attach(final_stop, last_leaf)
    for leaf in abjad.select.leaves(selections):
        literal_1 = abjad.LilyPondLiteral(
            r"\once \override Staff.Tie.transparent = ##t",
            site="before",
        )
        abjad.attach(literal_1, leaf)
        literal_2 = abjad.LilyPondLiteral(
            r"\once \override Dots.staff-position = #1.75",
            site="before",
        )
        abjad.attach(literal_2, leaf)
    abjad.glissando(selections, hide_middle_note_heads=True, allow_repeats=True, allow_ties=True)


def swells(selections):
    ties = abjad.select.logical_ties(selections)
    tie_groups = abjad.select.partition_by_counts(ties, [3, 2], cyclic=True)
    cyc_dynamics = evans.CyclicList(["p", "f", "mp", "mf", "pp", "mf", "mp", "ff"], forget=False)
    cyc_hairpins = evans.CyclicList(["<", ">"], forget=False)
    for group in tie_groups:
        tie = group[0]
        dynamic = abjad.Dynamic(cyc_dynamics(r=1)[0])
        abjad.attach(dynamic, tie[0])
    for group in tie_groups[:-1]:
        tie = group[0]
        hairpin = abjad.StartHairpin(cyc_hairpins(r=1)[0])
        abjad.attach(hairpin, tie[0])


def limited_swells(selections):
    ties = abjad.select.logical_ties(selections)
    cyc_dynamics = evans.CyclicList(["pp", "mf"], forget=False)
    cyc_hairpins = evans.CyclicList(["<", ">"], forget=False)
    for tie in ties:
        dynamic = abjad.Dynamic(cyc_dynamics(r=1)[0])
        abjad.attach(dynamic, tie[0])
    for tie in ties[:-1]:
        hairpin = abjad.StartHairpin(cyc_hairpins(r=1)[0])
        abjad.attach(hairpin, tie[0])



maker = evans.SegmentMaker(
    instruments=ksvedati.instruments,
    names=[
        '"Violin I"',
        '"Violin II"',
        '"Viola"',
        '"Violoncello"',
    ],
    abbreviations=[
        '"vn. I"',
        '"vn. II"',
        '"va."',
        '"vc."',
    ],
    name_staves=True,
    fermata_measures=ksvedati.fermata_measures_01,
    commands=[
        evans.attach(
            "violin 1 voice",
            abjad.Clef("treble"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "violin 2 voice",
            abjad.Clef("treble"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "viola voice",
            abjad.Clef("alto"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.attach(
            "cello voice",
            abjad.Clef("bass"),
            lambda _: abjad.select.leaf(_, 0),
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", 5),
            ],
            evans.talea(
                [3, 3, 2, 8],
                16,
                extra_counts=[0, 0, 2, 0, 3, 4, 0, 3, 2],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["a", "g'"]]),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "guiro (legno)" 1', site="after"),
            # evans.force_accidentals,
            evans.Callable(
                lambda _: baca.hairpin(_, "p < f"),
                selector=lambda _: abjad.select.leaves(_, pitched=True),
            ),
            # ksvedati.C_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", (8, 13)),
            ],
            evans.talea(
                [3, 2, 1, 3, 1, 2, 1, 2, 2, 3, 2],
                4,
                extra_counts=[1, 0, 1, -1, 0, 1],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["b'", "g''"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", (15, 19)),
            ],
            evans.talea(
                [3, 2, 8, 3],
                16,
                extra_counts=[0, 3, 4, 0, 3, 2, 0, 0, 2],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["a", "g'"]]),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "guiro (hair)" 1', site="after"),
            evans.Callable(
                lambda _: baca.hairpin(_, "p < f"),
                selector=lambda _: abjad.select.leaves(_, pitched=True),
            ),
            # ksvedati.C_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", (20, 23)),
            ],
            evans.talea(
                [_ * 2 for _ in [3, 2, 1, 3, 1, 2, 1, 2, 2, 3, 2]],
                16,
                extra_counts=[1, 0, 2, 1, -1, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 8] for _ in evans.Sequence([_ for _ in np.arange(-5, 24, 0.5)]).mirror(False).rotate(10).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=2,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", (24, 27)),
            ],
            evans.talea(
                [3, 2, 2, 4, 2],
                8,
                extra_counts=[0, 1, 3, 0, 1, 0, 1, 2],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["cs'", "b'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "tremoli" 1', site="after"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-one-markup -> \trem-three-markup -> \trem-two-markup -> \trem-five-markup -> \trem-four-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [3, 2, 4, 2], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [28, 29]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["fs'"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", 30),
            ],
            evans.talea(
                [2, 2, 4, 2, 3],
                8,
                extra_counts=[2, 0, 1, 3, 0, 1, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["cs'", "b'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-three-markup -> \trem-two-markup -> \trem-five-markup -> \trem-four-markup -> \trem-one-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [2, 3, 2, 4], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", 31),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["fs'"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [32, 33, 34]),
            ],
            evans.talea(
                [_ * 2 for _ in [2, 1, 3, 1, 2, 1, 2, 2, 3, 2, 3]],
                16,
                extra_counts=[1, 1, 0, 1, 2, -1, 0],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 9] for _ in evans.Sequence([_ for _ in np.arange(-5, 24, 0.5)]).mirror(False).rotate(14).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=3,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [35, 36, 37, 38, 39, 40]),
            ],
            evans.talea(
                [2, 8, 3, 3],
                16,
                extra_counts=[0, 3, 2, 0, 0, 2, 0, 3, 4],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["a", "g'"]]),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "guiro (hair) scratch poco a poco" 1', site="after"),
            evans.Callable(
                lambda _: baca.hairpin(_, "p < f"),
                selector=lambda _: abjad.select.leaves(_, pitched=True),
            ),
            # ksvedati.C_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [42, 43]),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["b'"]),
            abjad.Dynamic('"mf"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute col legno" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [44, 45, 46]),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["b'"]),
            abjad.Dynamic('"f"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute with hair" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("violin 1 voice", [48, 49, 50]),
            ],
            evans.talea(
                [1, 3, 1, 2, 1, 2, 2, 3, 2, 3, 2],
                4,
                extra_counts=[0, 1, 1, 0, 1, -1],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["b'", "g''"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [0, 1]),
            ],
            evans.tuplet(
                [(3, 1), (1,), (4, 1), (4, 2), (1,)],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True, fuse_counts=[1, 2, 1, 3, 1, 1, 2])
            ),
            evans.PitchHandler(["b'"]),
            abjad.Dynamic('"p"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on spike" 1', site="after"),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[0:2],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 2),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[3:5],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 5),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[6:8],
            ),
            lambda _: [abjad.attach(abjad.Tie(), pair[0]) for pair in abjad.select.partition_by_counts(abjad.select.exclude(abjad.select.leaves(_), [1, 4], 8), [2], cyclic=True)],
            # ksvedati.A_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [10, 11, 12]),
            ],
            evans.talea(
                [3, 1, 2, 1, 2, 2, 3, 2, 3, 2, 1],
                4,
                extra_counts=[-1, 0, 1, 1, 0, 1],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["e'", "c''"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [14, 15]),
            ],
            evans.talea(
                [1, 2, 1, 2, 2, 3, 2, 3, 2, 1, 3],
                4,
                extra_counts=[1, -1, 0, 1, 1, 0],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["e'", "c''"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [18, 19]),
            ],
            evans.talea(
                [2, 1, 2, 2, 3, 2, 3, 2, 1, 3, 1],
                4,
                extra_counts=[0, 1, -1, 0, 1, 1],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["e'", "c''"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [21, 22, 23]),
            ],
            evans.talea(
                [_ * 2 for _ in [1, 3, 1, 2, 1, 2, 2, 3, 2, 3, 2]],
                16,
                extra_counts=[0, 2, 1, 1, 0, 1, -1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 6] for _ in evans.Sequence([_ for _ in np.arange(-5, 24, 0.5)]).mirror(False).rotate(7).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=4,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [24, 25, 26]),
            ],
            evans.talea(
                [2, 4, 2, 3, 2],
                8,
                extra_counts=[1, 2, 0, 1, 3, 0, 1, 0],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["b", "a'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-two-markup -> \trem-five-markup -> \trem-four-markup -> \trem-one-markup -> \trem-three-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [4, 2, 3, 2], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [28, 29]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["gs"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", 30),
            ],
            evans.talea(
                [4, 2, 3, 2, 2],
                8,
                extra_counts=[0, 1, 2, 0, 1, 3, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["b", "a'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-five-markup -> \trem-four-markup -> \trem-one-markup -> \trem-three-markup -> \trem-two-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [2, 4, 2, 3], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", 31),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["gs"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [32, 33]),
            ],
            evans.talea(
                [_ * 2 for _ in [3, 1, 2, 1, 2, 2, 3, 2, 3, 2, 1]],
                16,
                extra_counts=[-1, 2, 0, 1, 2, 1, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 5] for _ in evans.Sequence([_ for _ in np.arange(-5, 24, 0.5)]).mirror(False).rotate(5).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=5,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [34, 35, 36, 37]),
            ],
            evans.tuplet(
                [(3, 1), (1,), (4, 1), (4, 2), (1,)],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True, fuse_counts=[1, 2, 1, 3, 1, 1, 2])
            ),
            evans.PitchHandler(["b'"]),
            abjad.Dynamic('"p"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on spike" 1', site="after"),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[0:2],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 2),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[3:5],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 5),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[6:8],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[8:10],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 10),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[11:13],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 13),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[14:16],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[16:18],
            ),
            lambda _: [abjad.attach(abjad.Tie(), pair[0]) for pair in abjad.select.partition_by_counts(abjad.select.exclude(abjad.select.leaves(_), [1, 4], 8), [2], cyclic=True)],
            # ksvedati.A_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [38, 39]),
            ],
            evans.talea(
                [_ * 2 for _ in [1, 2, 1, 2, 2, 3, 2, 3, 2, 1, 3]],
                16,
                extra_counts=[1, -1, 2, 0, 2, 1, 1, 0],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 7] for _ in evans.Sequence([_ for _ in np.arange(-5, 24, 0.5)]).mirror(False).rotate(3).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=6,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", [40, 41, 42]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["gs"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("violin 2 voice", (43, 53)),
            ],
            evans.tuplet(
                [(1,), (4, 1), (4, 2), (1,), (3, 1)],
                rewrite=-1,
                preprocessor=evans.make_preprocessor(quarters=True, fuse_counts=[2, 1, 2, 1, 3, 1, 1], split_at_measure_boundaries=True)
            ),
            evans.PitchHandler(["b'"]),
            abjad.Dynamic('"p"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on spike" 1', site="after"),

            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 0),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[1:3],
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[3:5],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 5),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[6:8],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 8),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[9:11],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[11:13],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 13),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[14:16],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 16),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[17:19],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[19:21],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 21),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[22:24],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 24),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[25:27],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[27:29],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-middle-markup"),
                    abjad.Tweak(r"\tweak staff-padding 5"),
                ),
                selector=lambda _: abjad.select.leaf(_, 29),
                direction=abjad.UP,
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
                pieces=lambda _: abjad.select.logical_ties(_)[30:32],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 32),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-bottom-markup -> \spike-middle-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[33:35],
            ),

            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[32:34],
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[34:36],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 36),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[37:40],
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[40:42],
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[42:44],
            ),
            evans.Attachment(
                abjad.bundle(
                    abjad.Markup(r"\spike-top-markup"),
                    abjad.Tweak(r"\tweak staff-padding 6"),
                ),
                selector=lambda _: abjad.select.leaf(_, 37),
                direction=abjad.UP,
            ),
            lambda _: baca.text_spanner(
                _,
                r"\spike-top-markup -> \spike-bottom-markup",
                abjad.Tweak(r"\tweak staff-padding 8.5"),
                # abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                # (abjad.Tweak(r"\tweak staff-padding 12"), 4),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=True,
                # leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.logical_ties(_)[44:46],
            ),

            lambda _: [abjad.attach(abjad.Tie(), pair[0]) for pair in abjad.select.partition_by_counts(abjad.select.exclude(abjad.select.leaves(_), [0, 5], 8), [2], cyclic=True)],
            # ksvedati.A_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [9, 10, 11]),
            ],
            evans.talea(
                [2, 4, 2, 3, 2],
                8,
                extra_counts=[0, 1, 0, 1, 2, 0, 1, 3],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["a", "g'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-four-markup -> \trem-one-markup -> \trem-three-markup -> \trem-two-markup -> \trem-five-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [3, 2, 4, 2], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", (15, 27)),
            ],
            evans.talea(
                [_ * 2 for _ in [2, 1, 2, 2, 3, 2, 3, 2, 1, 3, 1]],
                16,
                extra_counts=[2, 0, 1, -1, 0, 1, 2, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 10] for _ in evans.Sequence([_ for _ in np.arange(-12, 24, 0.5)]).mirror(False).rotate(16).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=7,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [28, 29]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["d"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", 30),
            ],
            evans.talea(
                [4, 2, 3, 2, 2],
                8,
                extra_counts=[3, 0, 1, 0, 1, 2, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["a", "g'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-one-markup -> \trem-three-markup -> \trem-two-markup -> \trem-five-markup -> \trem-four-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [2, 3, 2, 4], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", 31),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["d"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [32, 33, 34, 35]),
            ],
            evans.talea(
                [_ * 2 for _ in [1, 2, 2, 3, 2, 3, 2, 1, 3, 1, 2]],
                16,
                extra_counts=[1, 2, 0, 2, 1, 2, -1, 0, 1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 11] for _ in evans.Sequence([_ for _ in np.arange(-12, 24, 0.5)]).mirror(False).rotate(18).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=8,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [38, 39]),
            ],
            evans.talea(
                [_ * 2 for _ in [2, 2, 3, 2, 3, 2, 1, 3, 1, 2, 1]],
                16,
                extra_counts=[2, 1, 1, 2, 0, 1, -1, 2, 0],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 13] for _ in evans.Sequence([_ for _ in np.arange(-12, 24, 0.5)]).mirror(False).rotate(120).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=9,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [40, 41, 42, 43, 44, 45]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["d"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("viola voice", [47, 48, 49, 50]),
            ],
            evans.talea(
                [2, 2, 3, 2, 3, 2, 1, 3, 1, 2, 1],
                4,
                extra_counts=[1, 1, 0, 1, -1, 0],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["a", "f'"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [1, 2]),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["d"]),
            abjad.Dynamic('"f"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute col legno" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [4, 5]),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["d"]),
            abjad.Dynamic('"mp"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute with hair" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", (7, 13)),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["d"]),
            abjad.Dynamic('"mf"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute col legno" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", (15, 27)),
            ],
            evans.talea(
                [_ * 2 for _ in [2, 3, 2, 3, 2, 1, 3, 1, 2, 1, 2]],
                16,
                extra_counts=[2, 0, 2, 1, 2, 1, 2, 0, 1, -1],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 6] for _ in evans.Sequence([_ for _ in np.arange(-24, 24, 0.5)]).mirror(False).rotate(4).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=10,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [28, 29]),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["f,"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", 30),
            ],
            evans.talea(
                [2, 3, 2, 2, 4],
                8,
                extra_counts=[1, 3, 0, 1, 0, 1, 2, 0],
                preprocessor=evans.make_preprocessor(quarters=True),
                rewrite=-1,
            ),
            # lambda _: abjad.tie(_),
            evans.PitchHandler([["g", "f'"]]),
            lambda _: limited_swells(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            lambda _: baca.text_spanner(
                _,
                r"\trem-three-markup -> \trem-two-markup -> \trem-five-markup -> \trem-four-markup -> \trem-one-markup",
                abjad.Tweak(r"\tweak staff-padding 4"),
                abjad.Tweak(r"\tweak bound-details.right.padding 1.5"),
                final_piece_spanner=r"\stopTextSpanOne",
                autodetect_right_padding=False,
                bookend=False,
                leak_spanner_stop=True,
                lilypond_id=1,
                pieces=lambda _: abjad.select.partition_by_counts(abjad.select.logical_ties(_), [4, 2, 3, 2], cyclic=True, overhang=True),
            ),
            # ksvedati.E_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", (31, 38)),
            ],
            evans.tuplet(
                [(3, 1), (4, 1), (4, 2)],
                rewrite=-1,
            ),
            evans.PitchHandler(["f,"]),
            evans.NoteheadHandler(["harmonic"], forget=False, head_boolean_vector=[1]),
            lambda _: [baca.hairpin(x, "sfp < f") for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StartTrillSpan(interval=abjad.NamedInterval("P1")), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.StopTrillSpan(), abjad.get.leaf(x[-1], 1)) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            lambda _: [abjad.attach(abjad.Tie(), x[0]) for x in abjad.select.partition_by_counts(abjad.select.leaves(_, pitched=True), [2], cyclic=True, overhang=True)],
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bisbigliando" 1', site="after"),
            # abjad.Articulation("trill"),
            # ksvedati.G_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [38, 39]),
            ],
            evans.talea(
                [_ * 2 for _ in [3, 2, 3, 2, 1, 3, 1, 2, 1, 2, 2]],
                16,
                extra_counts=[-1, 2, 2, 0, 1, 2, 1, 0, 1, 2],
                preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler(
                [[_, _ + 8] for _ in evans.Sequence([_ for _ in np.arange(-24, 24, 0.5)]).mirror(False).rotate(8).random_walk(
                    length=100,
                    step_list=[2, 6, 4, 4],
                    random_seed=11,
                ).remove_repeats()]
            ),
            lambda _: swells(_),
            evans.zero_padding_glissando,
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            # abjad.LilyPondLiteral(r'\boxed-markup "gliss" 1', site="after"),
            # ksvedati.F_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [42, 43, 44]),
            ],
            evans.make_tied_notes(),
            evans.PitchHandler(["d"]),
            abjad.Dynamic('"f"'),
            abjad.LilyPondLiteral(r"\staff-line-count 1", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "bow on mute with hair" 1', site="after"),
            # ksvedati.B_color,
        ),
        evans.MusicCommand(
            [
                ("cello voice", [46, 47, 48, 49, 50]),
            ],
            evans.talea(
                [3, 2, 3, 2, 1, 3, 1, 2, 1, 2, 2],
                4,
                extra_counts=[-1, 0, 1, 1, 0, 1],
                # preprocessor=evans.make_preprocessor(quarters=True),
            ),
            evans.PitchHandler([["d", "bf"]]),
            lambda _: attach_material(_),
            abjad.LilyPondLiteral(r"\staff-line-count 5", site="absolute_before"),
            abjad.LilyPondLiteral(r'\boxed-markup "slow bow" 1', site="after"),
            # ksvedati.D_color,
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
            evans.select_measures([3], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([6], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([13], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.ufermata"',
            ),
            evans.select_measures([27], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.Markup(
                r'\markup \lower #9 \with-dimensions-from \null \musicglyph #"scripts.uverylongfermata"',
            ),
            evans.select_measures([53], leaf=1),
            direction=abjad.UP,
        ),
        evans.attach(
            "Global Context",
            abjad.LilyPondLiteral(r'\bar "|."', site="after"),
            evans.select_measures([53], leaf=1),
        ),
        evans.attach(
            "cello voice",
            abjad.Markup(r"\colophon"),
            lambda _: abjad.select.leaf(_, -3),
            direction=abjad.DOWN,
        ),
    ],
    score_template=ksvedati.score,
    transpose_from_sounding_pitch=True,
    time_signatures=ksvedati.signatures_01,
    clef_handlers=None,
    tuplet_bracket_noteheads=False,
    add_final_grand_pause=False,
    score_includes=[
        "abjad.ily",
        "../../build/segment_stylesheet.ily",
    ],
    segment_name="01",
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
