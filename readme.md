## Procedural art generator based on audio files

## How it works

    An audio file is opened and passed through the `processDataPipeline()` 
    function, which manipulates a data matrix to build an image based 
    on the following algorithm:

    Raw audio data is reshaped and mapped to form an RGB 2D matrix.
    |
    The matrix is sorted, and a color map is applied according to the original data values.
    |
    Certain portions are extruded according to BPM and beat patterns.
    |
    The entire image is distorted based on the original waveform and sample rate.
    |
    ASCII art is selected from the `\assets` archive based on 
    the given title and the original data values.
    |
    The chosen title is applied and colored according to the color map values.
    |
    Random noise is added based on the original data values.
    |
    Standard sharpening is applied.

## Credits 

    All ASCII art was sourced from the [awesome-ascii-art]
    (https://github.com/devtooligan/awesome-ascii-art.git) repository. 
    Authors should be credited in the images or in the repository's original files.