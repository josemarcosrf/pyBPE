// Example program
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <list>
#include <stdio.h>
#include <cstring>
#include <boost/python.hpp>

using namespace std;
namespace py = boost::python;       // this will allow to pass list between C++ and python

#define FALSE      0
#define TRUE       1
#define UNDEFINED -1


/*
    Fuzy–Levenshtein distance algorithm.
    ---------------------------------------

    Distance between two words is the minimum number of operations
    (consisting of insertions, deletions or substitutions of a single character)
    required to change one word into the other.

    We make it 'fuzzy' by allowing sub-string matching, this is, not counting
    as blanks insertions at the begining nor end of the pattern when matching
    the text.

    Note that this is not a distance extrictly speaking, does not hold the
    simetry property, thus is important to pass the pattern as a first argument.
*/
int fuzzy_lev(string pattern, string text)
{
    int len_p = pattern.size();
    int len_t = text.size();

    // empty strings?
    if (len_p == 0 or len_t == 0)
        return 0;

    // pattern is a character?
    else if (len_p == 1){
        bool found = (text.find(pattern) != string::npos);
        return !found;
    }

    // iterate over the Levenshtein distance 'matrix'
    vector<int> row1 (len_t + 1, 0);
    for (int i=0; i < len_p; i++){
        vector<int> row2(1, i+1);
        for (int j=0; j < len_t; j++){
            int cost = int(pattern[i] != text[j]);
            row2.push_back(min(row1[j + 1] + 1, min(row2[j] + 1, row1[j] + cost)));
        }
        row1 = row2;
    }
    return *min_element(row1.begin(), row1.end());  // distance
}


/*
    Backward Oracle Matching algorithm
    ----------------------------------

*/

// structure definitions: cell and linked list of cells for the transition graph
struct _cell{
    int element;
    struct _cell *next;
  };

typedef struct _cell *List;


int get_transition(string x, int p, List L[], char c) {
   List cell;

   if (p > 0 and x[p - 1] == c)
      return(p - 1);
   else {
      cell = L[p];
      while (cell != NULL)
         if (x[cell->element] == c)
            return(cell->element);
         else
            cell = cell->next;
      return(UNDEFINED);
   }
}


void set_transition(int p, int q, List L[]) {
   List cell;

   cell = (List)malloc(sizeof(struct _cell));
   if (cell == NULL)
      cout << "BOM/set_transition" << endl;
   cell->element = q;
   cell->next = L[p];
   L[p] = cell;
}


void oracle(string x, int m, char T[], List L[]) {
   int i, p, q;
   int S[x.size() + 1];
   char c;

   S[m] = m + 1;
   for (i = m; i > 0; --i) {
      c = x[i - 1];
      p = S[i];
      while (p <= m && (q = get_transition(x, p, L, c)) == UNDEFINED) {
         set_transition(p, i - 1, L);
         p = S[p];
      }
      S[i - 1] = (p == m + 1 ? m : q);
   }
   p = 0;
   while (p <= m) {
      T[p] = TRUE;
      p = S[p];
   }
}


py::list bom_search(string x, int m, string y, int n) {
   char T[x.size() + 1];
   List L[x.size() + 1];
   int i, j, p, period, q, shift;       // pointers for current position and shifts
   py::list pointers;                   // solutions list

   /* Preprocessing */
   memset(L, NULL, (m + 1) * sizeof(List));
   memset(T, FALSE, (m + 1) * sizeof(char));
   oracle(x, m, T, L);

   /* Searching */
   j = 0;
   while (j <= n - m) {
      i = m - 1;
      p = m;
      shift = m;
      while (i + j >= 0 &&
            (q = get_transition(x, p, L, y[i + j])) != UNDEFINED) {
         p = q;
         if (T[p] == TRUE) {
            period = shift;
            shift = i;
         }
         --i;
      }
      if (i < 0) {
         pointers.append(j);    // if using list: pointer.push_back(j)
         shift = period;
      }
      j += shift;
   }
   return pointers;
}



/*
    Required to expose the fucntions.
    macro Boost.Python provides to signify a Python extension module
*/
#include <boost/python.hpp>

BOOST_PYTHON_MODULE(libbasic_text) {
    // An established convention for using boost.python.
    using namespace boost::python;

    // Expose the functions.
    def("fuzzy_lev", fuzzy_lev);
    def("bom_search", bom_search);
}



/* To compile and execute as c++:
    - change py::list for c++ list<int> everywhere in the code
    - in 'bom_search' use: 'pointers.push_back(j)' instead of 'pointers.append(j)'

    If not intended to use from c++ directly (using as wrapper)
    the main function should remain commented out
*/

// int main(){
//     string pattern = "ABCD";
//     string text = "askjdhasasdalkdaisdabcdasdABCDasdasdasdethtujabcdkojpy";

//     py::list pointers = bom_search(pattern, pattern.size(), text, text.size());

//     bool any = (pointers.size() > 0);
//     if (any)
//         for (list::iterator it = pointers.begin(); it != pointers.end(); it++){
//             cout << "pointer: " << *it << endl;
//         }
//     else
//         cout << "no pointers found" << endl;
// }
