\version "2.22.1"  %2.23.2
\language "english" %! LilyPondFile

\include "../parts_stylesheet_duet.ily"                                      %! LilyPondFile
\include "abjad.ily" %! LilyPondFile

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\score{
    <<
        { \include "layout.ly" }
    	{
            \include "02.ly"
    	}
    >>
%{ \midi{} %}
}
