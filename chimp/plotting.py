import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse
import numpy as np


def plot_hit_hists(fia, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))
    non_mut_dists = fia.hit_dists(fia.non_mutual_hits)
    bins = np.linspace(0, max(non_mut_dists), 50)

    if non_mut_dists:
        ax.hist(non_mut_dists, bins, label='Non-mutual hits', normed=True, histtype='step')
    if fia.bad_mutual_hits:
        ax.hist(fia.hit_dists(fia.bad_mutual_hits), bins,
                label='Bad mutual hits', normed=True, histtype='step')
    if fia.good_mutual_hits:
        ax.hist(fia.hit_dists(fia.good_mutual_hits), bins, label='Good mutual hits',
                normed=True, histtype='step')
    if fia.exclusive_hits:
        ax.hist(fia.hit_dists(fia.exclusive_hits), bins, label='Exclusive hits',
                normed=True, histtype='step')
    ax.legend()
    ax.set_title('%s Nearest Neighbor Distance Distributions' % fia.image_data.fname)
    return ax


def plot_hits(fia, hits, color, ax, kwargs={}):
    for i, j in hits:
        ax.plot([fia.sexcat.point_rcs[i, 1], fia.aligned_rcs_in_frame[j, 1]],
                [fia.sexcat.point_rcs[i, 0], fia.aligned_rcs_in_frame[j, 0]],
                color=color, **kwargs)
    return ax


def plot_ellipses(fia, ax, alpha=1.0, color=(1, 0, 0)):
    ells = [Ellipse(xy=(pt.c, pt.r), width=pt.width, height=pt.height, angle=pt.theta)
            for pt in fia.sexcat.points]
    for e in ells:
        ax.add_artist(e)
        e.set_alpha(alpha)
        e.set_facecolor(color)


def plot_all_hits(fia, ax=None, im_kwargs={}, line_kwargs={}, fqpt_kwargs={}, sext_kwargs={},
                 title_kwargs={}, legend_kwargs={}):
    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 15))

    kwargs = {'cmap': plt.get_cmap('Blues')}
    kwargs.update(im_kwargs)
    ax.matshow(fia.image_data.imageage, **kwargs)

    kwargs = {'color': 'k', 'alpha': 0.3, 'linestyle': '', 'marker': 'o', 'markersize': 3}
    kwargs.update(fqpt_kwargs)
    ax.plot(fia.aligned_rcs_in_frame[:, 1], fia.aligned_rcs_in_frame[:, 0], **kwargs)

    kwargs = {'alpha': 0.6, 'color': 'darkgoldenrod'}
    kwargs.update(sext_kwargs)
    fia.plot_ellipses(ax, **kwargs)

    fia.plot_hits(fia.non_mutual_hits, 'grey', ax, line_kwargs)
    fia.plot_hits(fia.bad_mutual_hits, 'b', ax, line_kwargs)
    fia.plot_hits(fia.good_mutual_hits, 'magenta', ax, line_kwargs)
    fia.plot_hits(fia.exclusive_hits, 'r', ax, line_kwargs)
    ax.set_title('All Hits: %s vs. %s %s\nRot: %s deg, Fq width: %s um, Scale: %s px/fqu, Corr: %s, SNR: %s'
            % (fia.image_data.fname,
               fia.experiment.project_name,
               ','.join(tile.key for tile in fia.hitting_tiles),
               ','.join('%.2f' % tile.rotation_degrees for tile in fia.hitting_tiles),
               ','.join('%.2f' % tile.width for tile in fia.hitting_tiles),
               ','.join('%.5f' % tile.scale for tile in fia.hitting_tiles),
               ','.join('%.1f' % tile.best_max_corr for tile in fia.hitting_tiles),
               ','.join('%.2f' % tile.snr if hasattr(tile, 'snr') else '-' for tile in fia.hitting_tiles),
               ), **title_kwargs)
    ax.set_xlim([0, fia.image_data.image.shape[1]])
    ax.set_ylim([fia.image_data.image.shape[0], 0])

    grey_line = Line2D([], [], color='grey',
            label='Non-mutual hits: %d' % (len(fia.non_mutual_hits)))
    blue_line = Line2D([], [], color='blue',
            label='Bad mutual hits: %d' % (len(fia.bad_mutual_hits)))
    magenta_line = Line2D([], [], color='magenta',
            label='Good mutual hits: %d' % (len(fia.good_mutual_hits)))
    red_line = Line2D([], [], color='red',
            label='Exclusive hits: %d' % (len(fia.exclusive_hits)))
    sexcat_line = Line2D([], [], color='darkgoldenrod', alpha=0.6, marker='o', markersize=10,
            label='Sextractor Ellipses: %d' % (len(fia.sexcat.point_rcs)))
    fastq_line = Line2D([], [], color='k', alpha=0.3, marker='o', markersize=10,
            label='Fastq Points: %d' % (len(fia.aligned_rcs_in_frame)))
    handles = [grey_line, blue_line, magenta_line, red_line, sexcat_line, fastq_line]
    legend = ax.legend(handles=handles, **legend_kwargs)
    legend.get_frame().set_color('white')
    return ax