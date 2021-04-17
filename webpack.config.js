const fs = require('fs')
const path = require('path')
const glob = require('glob-all')
const webpack = require('webpack')
const FriendlyErrorsWebpackPlugin = require('friendly-errors-webpack-plugin')
const WebpackNotifierPlugin = require('webpack-notifier')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const TerserPlugin = require('terser-webpack-plugin')
const PurgecssPlugin = require('purgecss-webpack-plugin')
const EventHooksPlugin = require('event-hooks-webpack-plugin')
const ErrorOverlayPlugin = require('error-overlay-webpack-plugin')

const eslintFormatter = require('react-dev-utils/eslintFormatter')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
const CompressionPlugin = require('compression-webpack-plugin')
const zlib = require('zlib')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
const WebpackPwaManifest = require('webpack-pwa-manifest')

const appDirectory = fs.realpathSync(process.cwd())
const resolveApp = relativePath => path.resolve(appDirectory, relativePath)
// resolveApp('src/app');

module.exports = env => {
    const isDevelopment = process.env.NODE_ENV === 'development'
    const isProduction = process.env.NODE_ENV === 'production'
    const devtool = isDevelopment ? 'cheap-module-source-map' : 'source-map'
    const profilingEnabled = false
    const createSourceMaps = true
    const DIST_DIR = path.resolve(__dirname, './tasks/static/dist')
    const SRC_DIR = path.resolve(__dirname, './tasks/src')
    const TEMPLATES_DIR = path.resolve(__dirname, './tasks/templates')

    return {
        mode: isDevelopment ? 'development' : 'production',
        bail: isProduction,
        entry: {
            app: path.join(SRC_DIR, 'app.js'),
        },
        output: {
            path: DIST_DIR,
            publicPath: '/',
            filename: isDevelopment ? 'js/[name].js' : 'js/[name].[contenthash:8].js',
            chunkFilename: isDevelopment ? 'js/[id].js' : 'js/[id].[contenthash:8].js',
        },

        devtool: isProduction ?
            createSourceMaps ?
                devtool :
                false : isDevelopment && devtool,

        module: {
            rules: [
                {
                    test: /\.html$/,
                    use: ['html-loader'],
                },
                {
                    test: /(\.(png|jpe?g|gif|webp)$|^((?!font).)*\.svg$)/,
                    use: [{
                        loader: 'url-loader',
                        options: {
                            outputPath: 'imgs',
                            // publicPath: '/',
                            limit: 8192,
                            quality: 85,
                            name: '[name].[hash:8].[ext]',
                            fallback: 'file-loader',
                            // useRelativePath: 'true',
                        },
                    },

                        {
                            loader: 'img-loader',
                            options: {
                                plugins: [
                                    // require('imagemin-mozjpeg')(),
                                    require('imagemin-pngquant')(),
                                    require('imagemin-gifsicle')(),
                                    require('imagemin-svgo')(),
                                ],
                            },
                        },
                    ],
                },
                {
                    test: /(\.(woff2?|ttf|eot|otf)$|font.*\.svg$)/,
                    use: [{
                        loader: 'file-loader',
                        options: {
                            // publicPath: '/dist/fonts/',
                            publicPath: '../fonts',
                            name: '[name].[hash:8].[ext]',
                            outputPath: 'fonts/',
                        },
                    }],
                },
                {
                    test: /\.(sa|sc|c)ss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: {
                                sourceMap: createSourceMaps,
                            },
                        },
                        {
                            loader: 'postcss-loader',
                            options: {

                                sourceMap: createSourceMaps,
                                postcssOptions: {
                                    config: path.resolve(__dirname, 'postcss.config.js'),
                                },
                            },
                        },
                        {
                            loader: 'resolve-url-loader',
                            options: {
                                sourceMap: createSourceMaps,
                            },
                        },
                        {
                            loader: 'sass-loader',
                            options: isDevelopment ? {
                                sourceMap: createSourceMaps,
                            } : {sourceMap: createSourceMaps},
                        },
                    ],
                },
                {
                    test: /\.(js|jsx)$/,
                    // exclude: '/(node_modules)/',
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
            ].filter(Boolean),
        },
        plugins: [
            new webpack.ProgressPlugin(),
            new WebpackNotifierPlugin(),
            new FriendlyErrorsWebpackPlugin(),
            new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),

            new webpack.DefinePlugin({
                'NICE_FEATURE': JSON.stringify(true),
                'EXPERIMENTAL_FEATURE': JSON.stringify(false),
                'SERVICE_URL': JSON.stringify('https://dev.example.com'),
            }),

            new EventHooksPlugin({
                done: stats => {
                    const {
                        time,
                        errors,
                        assets,
                    } = stats.toJson()
                    let assetCollection = {}
                    assets.forEach(({name}) => {
                        let ext = name.split('.').reverse()[0]
                        if (['css', 'js'].includes(ext)) {
                            let key = `${name.substring(
                                0,
                                name.indexOf('.'),
                            )}.${ext}`
                            Object.assign(assetCollection, {
                                [key]: name,
                            })
                        }
                    })
                    fs.writeFileSync(path.join(DIST_DIR, "assets-manifest.json"),
                        JSON.stringify(assetCollection, null, 2),
                    )
                },
            }),

            isProduction && new CleanWebpackPlugin(),
            new MiniCssExtractPlugin({
                // path: path.resolve(__dirname, 'dist/css'),
                filename: isProduction ? 'css/[name].[contenthash:8].css' : 'css/[name].css',
                chunkFilename: isProduction ? 'css/[id].[contenthash:8].css' : 'css/[id].css',
            }),

            profilingEnabled && new BundleAnalyzerPlugin(),


            isProduction && new PurgecssPlugin({
                paths: glob.sync(
                    [
                        SRC_DIR + '/*.html',
                        SRC_DIR + '/**/*.jsx',
                        SRC_DIR + '/**/*.js',
                        TEMPLATES_DIR + '/**/*.html'
                    ], {nodir: true}),
            }),

            isDevelopment && new webpack.HotModuleReplacementPlugin(),

            isProduction && new CompressionPlugin({
                filename: '[path][base].gz',
                algorithm: 'gzip',
                test: /\.js$|\.css$|\.html$/,
                threshold: 10240,
                minRatio: 0.8,
            }),

            isProduction && new CompressionPlugin({
                filename: '[path][base].br',
                algorithm: 'brotliCompress',
                test: /\.(js|css|html|svg)$/,
                compressionOptions: {
                    params: {
                        [zlib.constants.BROTLI_PARAM_QUALITY]: 11,
                    },
                },
                threshold: 10240,
                minRatio: 0.8,
            }),

        ].filter(Boolean),
        // performance: false,
        performance: {
            hints: false,
            maxEntrypointSize: 512000,
            maxAssetSize: 512000,
        },
        stats: {
            hash: false,
            version: false,
            timings: false,
            children: false,
            errorDetails: false,
            entrypoints: false,
            performance: !isDevelopment,
            chunks: false,
            modules: false,
            reasons: false,
            source: false,
            publicPath: false,
            builtAt: false,
        },

        optimization: {
            minimize: isProduction,
            moduleIds: 'natural',//deterministic
            // chunkIds: false,
            minimizer: [
                new CssMinimizerPlugin({
                    cache: true,
                    parallel: true,
                    sourceMap: createSourceMaps,
                    minimizerOptions: {
                        preset: [
                            'default',
                            {
                                discardComments: {removeAll: true},
                            },
                        ],
                    },
                }),

                new TerserPlugin({
                    // cache: true,
                    parallel: true,
                    // sourceMap: createSourceMaps,
                    terserOptions: {
                        parse: {
                            ecma: 8,
                        },
                        compress: {
                            ecma: 5,
                            warnings: false,
                            comparisons: false,
                            inline: 2,
                        },
                        output: {
                            ecma: 5,
                            comments: false,
                            ascii_only: true,
                        },
                        mangle: {
                            safari10: true,
                        },
                    },
                }),
            ],

            splitChunks: {
                // include all types of chunks
                chunks: 'all',
                name: 'vendor',
                // maxInitialRequests: Infinity,
                // minSize: 0,
                // cacheGroups: {
                //     vendor: {
                //         chunks: 'initial',
                //         name: 'vendor',
                //         test: 'vendor',
                //         enforce: true
                //     },
                // }
            },
        },

        resolve: {
            extensions: ['.js', '.json', '.vue', '.scss', '.jsx', '*'],
            alias: {
                '@': path.resolve(__dirname, 'src'),
                'imgs': path.resolve(__dirname, 'src/assets/imgs/'),
                'sass': path.resolve(__dirname, 'src/assets/scss/'),
            },
        },
    }
}
