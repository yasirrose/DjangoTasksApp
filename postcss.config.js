module.exports = {
  plugins: [
    require('postcss-simple-vars'),
	require('postcss-nested'),
	require('postcss-import'),
	require('postcss-custom-media'),
	require('postcss-media-minmax'),
	require('postcss-flexbugs-fixes'),
	require('postcss-preset-env'),
	require('postcss-custom-selectors'),
	require('postcss-color-function'),
	require('autoprefixer'),
	require('precss'),
	require('postcss-normalize')
  ]
}