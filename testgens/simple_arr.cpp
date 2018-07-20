#ifdef LOCKAL
    #define _GLIBCXX_DEBUG
#endif
#ifndef LOCKAL
    #pragma GCC optimize("Ofast")
    #pragma GCC target("sse3,sse4")
#endif
#include <bits/stdc++.h>
//#define TIMUS
//#define FILENAME "journey"
#ifndef TIMUS
    #include <ext/rope>
    #include <ext/pb_ds/assoc_container.hpp>
#endif // TIMUS
#define all(x) x.begin(), x.end()
#define F first
#define S second
#define pb push_back
#define pii pair<int, int>

typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;

const int INF = INT_MAX / 2;
const ll LINF = (ll)2e18 + 666, M = 1e9 + 7;
const ld EPS = 1e-7;

#ifndef M_PI
    const ld M_PI = acos(-1);
#endif // M_PI

using namespace std;

#ifndef TIMUS
    using namespace __gnu_cxx;
    using namespace __gnu_pbds;

    template<class K, class T>
    using ordered_map = tree<K, T, less<K>, rb_tree_tag, tree_order_statistics_node_update>;

    template<class T>
    using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
#endif

void run();

template<class T1, class T2>
inline bool mini(T1 &a, T2 b)
{
    if (a > b)
    {
        a = b;
        return 1;
    }
    return 0;
}

template<class T1, class T2>
inline bool maxi(T1 &a, T2 b)
{
    if (a < b)
    {
        a = b;
        return 1;
    }
    return 0;
}

int main(int argc, char **argv)
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    char c[4];
    ifstream f("/dev/urandom");
    for (int i = 0; i < 4; i++)
        f >> c[i];
    f.close();
    srand(*((int*)c));
    if (argc < 2)
        return 0;
    int n = rand() % atoi(argv[1]) + 1;
    cout << n;
    for (int i = 0; i < (argc >= 3 ? atoi(argv[2]) : 0); i++)
        cout << " " << rand() % n + 1;
    cout << "\n";
    for (int i = 0; i < n; i++)
        cout << rand() % 10 + 1 << " ";
    return 0;
}
