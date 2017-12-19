#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>

struct Dot {
    int xCo, yCo;

    Dot(int xCo, int yCo) : xCo(xCo), yCo(yCo) {}

    bool operator==(const Dot &rhs) const {
        return xCo == rhs.xCo &&
               yCo == rhs.yCo;
    }

    bool operator!=(const Dot &rhs) const {
        return !(rhs == *this);
    }
};

bool xBasedCmp(const Dot &a, const Dot &b) {
    return a.xCo != b.xCo ? a.xCo < b.xCo : a.yCo < b.yCo;
}

/**
 * Rotate vectors ab -> ac
 *  < 0 : right turn
 *  < 0 : left turn
 */
int rotate(const Dot &a, const Dot &b, const Dot &c) {
    long long angle = 1LL * (b.xCo - a.xCo) * (c.yCo - a.yCo) -
                      1LL * (b.yCo - a.yCo) * (c.xCo - a.xCo);
    if (angle < 0) {
        return -1;
    }
    if (angle > 0) {
        return 1;
    }
    return 0;
}

class GrahamConvexHullBuilder {

    std::vector<Dot> upperHull;
    std::vector<Dot> lowerHull;
    Dot leftestDot;

    void addToUpperHull(Dot &dot) {
        int upSize = upperHull.size();
        while (upperHull.size() >= 2 && rotate(
                upperHull[upSize - 1],
                upperHull[upSize - 2], dot) <= 0) {
            upperHull.pop_back();
            upSize--;
        }
        upperHull.push_back(dot);
    }

    void addToLowerHull(Dot &dot) {
        int lowSize = lowerHull.size();
        while (lowerHull.size() >= 2 && rotate(
                lowerHull[lowSize - 1],
                lowerHull[lowSize - 2], dot) >= 0) {
            lowerHull.pop_back();
            lowSize--;
        }
        lowerHull.push_back(dot);
    }

    std::vector<Dot> mergeHulls() {
        std::vector<Dot> convexHull(lowerHull);
        for (int i = upperHull.size() - 1; i >= 0; --i) {
            convexHull.push_back(upperHull[i]);
        }
        return convexHull;
    }

public:
    GrahamConvexHullBuilder() : leftestDot(Dot(0, 0)) {}

    std::vector<Dot> buildConvexHull(std::vector<Dot> &dots) {
        upperHull.clear();
        lowerHull.clear();

        std::sort(dots.begin(), dots.end(), &xBasedCmp);
        leftestDot = dots[0];
        Dot rightestDot = dots[dots.size() - 1];

        addToUpperHull(leftestDot);
        addToLowerHull(leftestDot);

        for (int i = 1; i < dots.size() - 1; ++i) {
            if (rotate(leftestDot, rightestDot, dots[i]) > 0) {
                addToUpperHull(dots[i]);
            } else {
                addToLowerHull(dots[i]);
            }
        }

        addToUpperHull(rightestDot);
        addToLowerHull(rightestDot);

        // remove first and last dot from lower hull
        lowerHull.erase(lowerHull.begin());
        lowerHull.pop_back();

        return mergeHulls();
    }

    const std::vector<Dot> &getUpperHull() const {
        return upperHull;
    }

    const std::vector<Dot> &getLowerHull() const {
        return lowerHull;
    }

    const Dot &getLeftestDot() const {
        return leftestDot;
    }
};


class ChanConvexHullBuilder {

    std::vector<Dot> dots;
    std::vector<Dot> hull;

    std::vector<std::vector<Dot> > grahamHulls;
    Dot leftestDot;
    int hullWithLeftestDot;

    GrahamConvexHullBuilder grahamBuilder;

    /**
     * Returns index of dot that has the right tangent line from p to hull.
     */
    int find_rightest(std::vector<Dot> &batch_hull, Dot p) {
        int left = 0;
        int right = batch_hull.size();

        while (right - left > 1) {
            int c = (left + right) / 2;

            int c_next_index = (c + 1) % batch_hull.size();
            int c_next = rotate(p, batch_hull[c], batch_hull[c_next_index]);

            int c_prev_index = (c - 1 + batch_hull.size()) % batch_hull.size();
            int c_prev = rotate(p, batch_hull[c], batch_hull[c_prev_index]);

            if (c_next >= 0 && c_prev >= 0) {
                return c;
            }

            // check which pointer to move
            int c_side = rotate(p, batch_hull[left], batch_hull[c]);

            int l_next_index = (left + 1) % batch_hull.size();
            int l_next = rotate(p, batch_hull[left], batch_hull[l_next_index]);

            int l_prev_index = (left - 1 + batch_hull.size()) % batch_hull.size();
            int l_prev = rotate(p, batch_hull[left], batch_hull[l_prev_index]);

            if ((c_side > 0) && (l_next < 0 || l_prev == l_next) || (c_side < 0 && c_prev < 0)) {
                right = c;
            } else {
                left = c + 1;
            }
        }

        return left;
    }

    bool build_convex_hull_batch(int batch_size) {
        build_graham_hulls_for_batches(batch_size);

        hull.clear();
        hull.push_back(leftestDot);

        int hull_taken = hullWithLeftestDot;
        int dot_taken = grahamHulls[hull_taken].size() - 1;

        for (int k = 0; k < batch_size; ++k) {
            Dot last_in_hull = hull[hull.size() - 1];
            dot_taken = (dot_taken + 1) % grahamHulls[hull_taken].size();
            Dot nextDot = grahamHulls[hull_taken][dot_taken];

            int hullInThisStep = hull_taken;
            for (int i = 0; i < grahamHulls.size(); ++i) {
                if (i == hull_taken) {
                    continue;
                }

                int rightestDotIndex = find_rightest(grahamHulls[i], last_in_hull);
                Dot rightestDot = grahamHulls[i][rightestDotIndex];

                if (rotate(last_in_hull, nextDot, rightestDot) < 0) {
                    nextDot = rightestDot;
                    dot_taken = rightestDotIndex;
                    hullInThisStep = i;
                }
            }

            if (nextDot == leftestDot) {
                return true;
            }
            hull.push_back(nextDot);
            hull_taken = hullInThisStep;
        }
        return false;
    }

    /**
     * Build convex hull for every batch from dots and store them in grahamHulls field
     * @param batch_size
     */
    void build_graham_hulls_for_batches(int batch_size) {
        leftestDot = dots[0];
        hullWithLeftestDot = 0;

        // build convex hulls for every batch
        grahamHulls.clear();
        int start = 0, end = batch_size;
        int hullNum = 0;

        while (start < dots.size()) {

            std::vector<Dot> batch;
            for (int i = start; i < end; ++i) {
                batch.push_back(dots[i]);
            }

            grahamHulls.push_back(grahamBuilder.buildConvexHull(batch));
            if (xBasedCmp(grahamBuilder.getLeftestDot(), leftestDot)) {
                leftestDot = grahamBuilder.getLeftestDot();
                hullWithLeftestDot = hullNum;
            }

            start = end;
            end = std::min(end + batch_size, (int) dots.size());
            hullNum++;
        }
    }

public:
    ChanConvexHullBuilder() : leftestDot(Dot(0, 0)), hullWithLeftestDot(0) {
        grahamBuilder = GrahamConvexHullBuilder();
    }

    std::vector<Dot> build_convex_hull(std::vector<Dot> &dots) {
        this->dots = dots;
        for (int t = 1; t < dots.size(); ++t) {
            // batch_size = 2 ^ (2 ^ t)
            int batch_size = static_cast<int>(pow(2, pow(2, t)));

            if (batch_size > dots.size()) {
                batch_size = dots.size();
            }

            hull.clear();
            bool is_built = build_convex_hull_batch(batch_size);
            if (is_built) {
                return hull;
            }
        }
    }
};

int main() {

    freopen("in.txt", "r", stdin);
    freopen("output.txt", "w", stdout);

    std::vector<Dot> dots;
    int x, y, n;

    std::cin >> n;
    for (int i = 0; i < n; ++i) {
        std::cin >> x >> y;
        dots.emplace_back(x, y);
    }

    ChanConvexHullBuilder builder;
    std::vector<Dot> hull = builder.build_convex_hull(dots);

    std::cout << hull.size() << "\n";
    for (int i = 0; i < hull.size(); ++i) {
        std::cout << hull[i].xCo << " " << hull[i].yCo << "\n";
    }
}
